from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .throttles import LoginRateThrottle
from .models import LoginAttempt, UserActivity
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view with rate limiting and login tracking
    """
    throttle_classes = [LoginRateThrottle]
    
    def post(self, request, *args, **kwargs):
        try:
            # Add additional logging
            print(f"Login attempt: {request.data}")
            
            # Extract credentials for tracking
            username = request.data.get('username', '')
            email = request.data.get('email', '')
            
            # If email is provided but username isn't, try to find the user by email
            if email and not username:
                try:
                    user = User.objects.get(email=email)
                    # Create a copy of the request data
                    modified_data = request.data.copy()
                    # Add the username to the request data
                    modified_data['username'] = user.username
                    request._full_data = modified_data
                    print(f"Found user by email: {user.username}")
                except User.DoesNotExist:
                    print(f"No user found with email: {email}")
            
            # Get the IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR', '')
                
            # Try to get the response from the parent class
            response = super().post(request, *args, **kwargs)
            
            # Log successful response
            print(f"Login successful: {response.data}")
            
            # If we get a 200 response, the login was successful
            if response.status_code == 200:
                try:
                    # Find the user that logged in - first try username, then email
                    user = None
                    if username:
                        user = User.objects.get(username=username)
                    elif email:
                        user = User.objects.get(email=email)
                    
                    if user:
                        # Update last login IP
                        user.last_login_ip = ip
                        user.save(update_fields=['last_login_ip'])
                        
                        # Log successful login
                        LoginAttempt.objects.create(
                            user=user,
                            ip_address=ip,
                            successful=True
                        )
                        
                        # Log login activity
                        UserActivity.objects.create(
                            user=user,
                            activity_type='login',
                            ip_address=ip
                        )
                        
                        # Add user info to response
                        user_data = {
                            'id': str(user.id),
                            'username': user.username,
                            'email': user.email,
                            'is_staff': user.is_staff,
                            'is_verified': user.is_verified
                        }
                        response.data['user'] = user_data
                except User.DoesNotExist:
                    pass  # Should not happen since login succeeded
                    
            return response
        except Exception as e:
            # Log any exceptions during login
            print(f"Login error: {str(e)}")
            raise


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh view
    """
    pass  # Add custom logic here if needed in the future
