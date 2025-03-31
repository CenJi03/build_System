import pytest
from rest_framework.test import APIClient
from authentication.models import CustomUser

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    """Create an admin user for testing"""
    admin = CustomUser.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='Admin@123',
        is_verified=True
    )
    return admin

@pytest.fixture
def regular_user():
    """Create a regular user for testing"""
    user = CustomUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='Test@123',
        is_verified=True
    )
    return user

@pytest.fixture
def admin_authenticated_client(api_client, admin_user):
    """Return an authenticated client with admin credentials"""
    url = '/api/auth/token/'
    response = api_client.post(url, {
        'username': 'admin',
        'password': 'Admin@123'
    }, format='json')
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture
def user_authenticated_client(api_client, regular_user):
    """Return an authenticated client with regular user credentials"""
    url = '/api/auth/token/'
    response = api_client.post(url, {
        'username': 'testuser',
        'password': 'Test@123'
    }, format='json')
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client