from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import LoginAttempt, UserActivity, TOTPDevice
from .totp import create_totp_device, generate_totp_uri, confirm_totp_device, verify_totp_token
from .two_factor_serializers import TOTPSetupSerializer, TOTPVerifySerializer, TOTPDisableSerializer
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer, 
    PasswordChangeSerializer,
    PasswordResetRequestSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset handling user-related operations
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Custom permission mapping
        - create: Admin users only (registration)
        - reset_password_request, verify_email, reset_password_confirm: Allow any user
        - Other actions: Require authentication
        """
        if self.action in ['create', 'deactivate_account']:
            permission_classes = [IsAdminUser]
        elif self.action in ['reset_password_request', 'verify_email', 'reset_password_confirm']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        elif self.action == 'reset_password_request':
            return PasswordResetRequestSerializer
        elif self.action == 'setup_2fa':
            return TOTPSetupSerializer
        elif self.action == 'verify_2fa':
            return TOTPVerifySerializer
        elif self.action == 'disable_2fa':
            return TOTPDisableSerializer
        return UserProfileSerializer

    def create(self, request):
        """
        User registration endpoint - Admin only
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate email verification token
        verification_token = get_random_string(length=32)
        user.email_verification_token = verification_token
        user.save()
        
        # Send verification email
        try:
            verification_link = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
            send_mail(
                'Verify Your Email',
                f'Click the link to verify your email: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log email sending failure
            print(f"Failed to send verification email: {e}")
        
        # Log user registration activity
        UserActivity.objects.create(
            user=user,
            activity_type='registration',
            ip_address=self.get_client_ip(request),
            additional_info={'created_by': request.user.username}
        )
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'User registered successfully. Verification email sent.'
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change password for authenticated user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log password change activity
        UserActivity.objects.create(
            user=user,
            activity_type='password_change',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def reset_password_request(self, request):
        """
        Request a password reset by sending a token via email
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            # Generate a random token
            token = get_random_string(length=32)
            # Store token with the user
            user.password_reset_token = token
            user.save()
            
            # Send email with reset link
            reset_url = f"{settings.FRONTEND_URL}/reset-password/?token={token}"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            # Log password reset request activity
            UserActivity.objects.create(
                user=user,
                activity_type='password_reset_request',
                ip_address=self.get_client_ip(request)
            )
            
            return Response({
                'message': 'Password reset link sent to your email'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            # We still return OK for security reasons
            return Response({
                'message': 'Password reset link sent to your email'
            }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def reset_password_confirm(self, request):
        """
        Reset password using token received via email
        """
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not token or not new_password:
            return Response({
                'error': 'Token and new password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(password_reset_token=token)
            
            # Validate password
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return Response({'error': list(e)}, status=status.HTTP_400_BAD_REQUEST)
                
            user.set_password(new_password)
            user.password_reset_token = None  # Clear the token after use
            user.save()
            
            # Log password reset activity
            UserActivity.objects.create(
                user=user,
                activity_type='password_reset',
                ip_address=self.get_client_ip(request)
            )
            
            return Response({
                'message': 'Password reset successful'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        """
        Verify email using token
        """
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email_verification_token=token)
            user.is_verified = True
            user.email_verification_token = None  # Clear the token
            user.save()
            
            # Log email verification
            UserActivity.objects.create(
                user=user,
                activity_type='email_verification',
                ip_address=self.get_client_ip(request)
            )
            
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def deactivate_account(self, request, pk=None):
        """
        Deactivate user account - Admin only
        """
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.save()
            
            # Log account deactivation
            UserActivity.objects.create(
                user=user,
                activity_type='account_deletion',
                ip_address=self.get_client_ip(request),
                additional_info={'deactivated_by': request.user.username}
            )
            
            return Response({'message': 'Account deactivated successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def setup_2fa(self, request):
        """
        Set up two-factor authentication for the user
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user already has a device
        existing_device = TOTPDevice.objects.filter(user=user).first()
        if existing_device and existing_device.confirmed:
            return Response({
                'error': 'Two-factor authentication is already set up'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Delete any existing unconfirmed devices
        TOTPDevice.objects.filter(user=user, confirmed=False).delete()
        
        # Create a new device
        device_name = serializer.validated_data.get('device_name', 'Default')
        device = create_totp_device(user, name=device_name)
        
        # Generate the URI for QR code
        uri = generate_totp_uri(user.username, device.key)
        
        return Response({
            'secret': device.key,
            'uri': uri,
            'message': 'Two-factor authentication setup started. Please verify with a token.'
        })
        
    @action(detail=False, methods=['post'])
    def verify_2fa(self, request):
        """
        Verify a TOTP token to complete 2FA setup
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        # Get the user's device
        device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
        if not device:
            return Response({
                'error': '2FA setup not started or already confirmed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Try to confirm the device
        if confirm_totp_device(device, token):
            # Update user's 2FA status
            user.two_factor_enabled = True
            user.save()
            
            # Log 2FA enabled
            UserActivity.objects.create(
                user=user,
                activity_type='2fa_enabled',
                ip_address=self.get_client_ip(request)
            )
            
            return Response({
                'message': 'Two-factor authentication enabled successfully'
            })
        else:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def disable_2fa(self, request):
        """
        Disable two-factor authentication for the user
        Requires password and current TOTP token for security
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verify password
        if not user.check_password(serializer.validated_data['password']):
            return Response({
                'error': 'Incorrect password'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Get the user's device
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if not device:
            return Response({
                'error': 'Two-factor authentication not enabled'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Verify token
        token = serializer.validated_data['token']
        if not verify_totp_token(device.key, token):
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Disable 2FA
        user.two_factor_enabled = False
        user.save()
        
        # Delete all TOTP devices
        TOTPDevice.objects.filter(user=user).delete()
        
        # Log 2FA disabled
        UserActivity.objects.create(
            user=user,
            activity_type='2fa_disabled',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({
            'message': 'Two-factor authentication disabled successfully'
        })
        
    @action(detail=False, methods=['get'])
    def check_2fa_status(self, request):
        """
        Check if the user has 2FA enabled
        """
        user = request.user
        return Response({
            'enabled': user.two_factor_enabled
        })
    
    def get_client_ip(self, request):
        """
        Extract client IP address from request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip