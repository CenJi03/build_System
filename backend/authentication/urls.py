from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import UserViewSet
from .token_views import CustomTokenObtainPairView, CustomTokenRefreshView

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # JWT Token-related URLs
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom authentication-related URLs
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('change-password/', UserViewSet.as_view({'post': 'change_password'}), name='change-password'),
    path('reset-password-request/', UserViewSet.as_view({'post': 'reset_password_request'}), name='reset-password-request'),
    path('reset-password-confirm/', UserViewSet.as_view({'post': 'reset_password_confirm'}), name='reset-password-confirm'),
    path('verify-email/', UserViewSet.as_view({'post': 'verify_email'}), name='verify-email'),
    path('user/<uuid:pk>/deactivate/', UserViewSet.as_view({'delete': 'deactivate_account'}), name='deactivate-account'),
    
    # Two-factor authentication endpoints
    path('setup-2fa/', UserViewSet.as_view({'post': 'setup_2fa'}), name='setup-2fa'),
    path('verify-2fa/', UserViewSet.as_view({'post': 'verify_2fa'}), name='verify-2fa'),
    path('disable-2fa/', UserViewSet.as_view({'post': 'disable_2fa'}), name='disable-2fa'),
    path('check-2fa-status/', UserViewSet.as_view({'get': 'check_2fa_status'}), name='check-2fa-status'),
]