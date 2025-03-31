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
        # Extract credentials for tracking
        username = request.data.get('username', '')
        
        # Get the IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
            
        # Try to get the response from the parent class
        response = super().post(request, *args, **kwargs)
        
        # If we get a 200 response, the login was successful
        if response.status_code == 200:
            try:
                # Find the user that logged in
                user = User.objects.get(username=username)
                
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
            except User.DoesNotExist:
                pass  # Should not happen since login succeeded
        else:
            # Log failed login attempt
            try:
                user = User.objects.filter(username=username).first()
                LoginAttempt.objects.create(
                    user=user,  # May be None if username doesn't exist
                    ip_address=ip,
                    successful=False
                )
            except Exception:
                pass  # Don't let logging errors affect the response
                
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh view
    """
    pass  # Add custom logic here if needed in the future
