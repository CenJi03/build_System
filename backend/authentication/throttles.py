from rest_framework.throttling import SimpleRateThrottle

class LoginRateThrottle(SimpleRateThrottle):
    """
    Throttle for login attempts based on IP address
    Limits login attempts to the rate specified in settings (default: 5/hour)
    """
    scope = 'login'
    
    def get_cache_key(self, request, view):
        # Use the IP address as the cache key
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class PasswordResetRateThrottle(SimpleRateThrottle):
    """
    Throttle for password reset requests based on IP address
    Limits password reset requests to the rate specified in settings (default: 3/hour)
    """
    scope = 'password_reset'
    
    def get_cache_key(self, request, view):
        # Use the IP address as the cache key
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class EmailVerificationRateThrottle(SimpleRateThrottle):
    """
    Throttle for email verification attempts based on IP address
    Limits verification attempts to the rate specified in settings (default: 10/hour)
    """
    scope = 'email_verification'
    
    def get_cache_key(self, request, view):
        # Use the IP address as the cache key
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }