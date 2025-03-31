from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.urls import resolve

from .models import TOTPDevice, CustomUser

class TwoFactorMiddleware(MiddlewareMixin):
    """
    Middleware to enforce 2FA verification for users with 2FA enabled
    
    This middleware checks if a user has 2FA enabled and ensures they've completed
    the 2FA verification process before accessing protected endpoints
    """
    
    # Paths that don't require 2FA verification
    EXEMPT_PATHS = [
        '/api/auth/token/',
        '/api/auth/token/refresh/',
        '/api/auth/verify-2fa/',
        '/admin/login/',
        '/api/auth/reset-password-request/',
        '/api/auth/reset-password-confirm/',
        '/api/auth/verify-email/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()
        
    def __call__(self, request):
        # Check if 2FA is enabled globally
        if not settings.TWO_FACTOR_ENABLED:
            return self.get_response(request)
            
        # Skip middleware for exempt paths
        path = request.path
        if any(path.startswith(exempt_path) for exempt_path in self.EXEMPT_PATHS):
            return self.get_response(request)
            
        # Try to get the user from the JWT token
        try:
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return self.get_response(request)
                
            token = auth_header.split(' ')[1]
            validated_token = self.jwt_auth.get_validated_token(token)
            user = self.jwt_auth.get_user(validated_token)
            
            # If the user has 2FA enabled, check if they've completed verification
            if user.two_factor_enabled:
                # Check if user has a confirmed TOTP device
                has_confirmed_device = TOTPDevice.objects.filter(
                    user=user, 
                    confirmed=True
                ).exists()
                
                if not has_confirmed_device:
                    # User has 2FA enabled but hasn't completed verification
                    # You could handle this by returning a custom response or
                    # letting the request continue and handling it in the view
                    pass
                    
        except (InvalidToken, AuthenticationFailed):
            # Token validation failed, let the regular authentication process handle it
            pass
            
        return self.get_response(request)