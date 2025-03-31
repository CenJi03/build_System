from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

from .models import LoginAttempt, UserActivity
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
        """
        if self.action in ['create', 'reset_password']:
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
        return UserProfileSerializer

    def create(self, request):
        """
        User registration endpoint
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log user registration activity
        UserActivity.objects.create(
            user=user,
            activity_type='login',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'User registered successfully'
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
            # Store token with the user (you might want to create a separate model for this)
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
    def reset_password(self, request):
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