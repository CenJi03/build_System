from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import UserViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # JWT Token-related URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom authentication-related URLs
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('change-password/', UserViewSet.as_view({'post': 'change_password'}), name='change-password'),
    path('reset-password-request/', UserViewSet.as_view({'post': 'reset_password_request'}), name='reset-password-request'),
    path('verify-email/', UserViewSet.as_view({'post': 'verify_email'}), name='verify-email'),
]