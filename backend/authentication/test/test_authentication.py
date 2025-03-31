import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import uuid
from django.utils.crypto import get_random_string
from authentication.models import CustomUser, LoginAttempt, UserActivity, TOTPDevice
from authentication.totp import get_totp_token, create_totp_device

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
    url = reverse('token_obtain_pair')
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
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'testuser',
        'password': 'Test@123'
    }, format='json')
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.mark.django_db
class TestAuthentication:
    """Test authentication functionality"""
    
    def test_login_success(self, api_client, regular_user):
        """Test successful login"""
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {
            'username': 'testuser',
            'password': 'Test@123'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        
        # Check if login attempt was logged
        assert LoginAttempt.objects.filter(user=regular_user, successful=True).exists()
        
    def test_login_failure(self, api_client, regular_user):
        """Test failed login"""
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {
            'username': 'testuser',
            'password': 'WrongPassword'
        }, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Check if failed login attempt was logged
        assert LoginAttempt.objects.filter(user=regular_user, successful=False).exists()
    
    def test_token_refresh(self, api_client, regular_user):
        """Test token refresh functionality"""
        # First, get a token
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(login_url, {
            'username': 'testuser',
            'password': 'Test@123'
        }, format='json')
        
        refresh_token = login_response.data['refresh']
        
        # Then use the refresh token to get a new access token
        refresh_url = reverse('token_refresh')
        refresh_response = api_client.post(refresh_url, {
            'refresh': refresh_token
        }, format='json')
        
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
    
    def test_token_verify(self, api_client, regular_user):
        """Test token verification"""
        # First, get a token
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(login_url, {
            'username': 'testuser',
            'password': 'Test@123'
        }, format='json')
        
        access_token = login_response.data['access']
        
        # Verify the token
        verify_url = reverse('token_verify')
        verify_response = api_client.post(verify_url, {
            'token': access_token
        }, format='json')
        
        assert verify_response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration functionality"""
    
    def test_admin_can_register_user(self, admin_authenticated_client):
        """Test that an admin can register a new user"""
        url = reverse('user-register')
        response = admin_authenticated_client.post(url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewUser@123',
            'password2': 'NewUser@123'
        }, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.objects.filter(username='newuser').exists()
        
        # Check that the user is not verified yet
        new_user = CustomUser.objects.get(username='newuser')
        assert not new_user.is_verified
        assert new_user.email_verification_token is not None
    
    def test_regular_user_cannot_register(self, user_authenticated_client):
        """Test that a regular user cannot register new users"""
        url = reverse('user-register')
        response = user_authenticated_client.post(url, {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'NewUser@123',
            'password2': 'NewUser@123'
        }, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CustomUser.objects.filter(username='newuser2').exists()
    
    def test_password_validation(self, admin_authenticated_client):
        """Test password validation during registration"""
        url = reverse('user-register')
        
        # Test with mismatched passwords
        response = admin_authenticated_client.post(url, {
            'username': 'newuser3',
            'email': 'newuser3@example.com',
            'password': 'NewUser@123',
            'password2': 'DifferentPassword'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not CustomUser.objects.filter(username='newuser3').exists()
        
        # Test with a common password
        response = admin_authenticated_client.post(url, {
            'username': 'newuser3',
            'email': 'newuser3@example.com',
            'password': 'password123',
            'password2': 'password123'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not CustomUser.objects.filter(username='newuser3').exists()

@pytest.mark.django_db
class TestEmailVerification:
    """Test email verification functionality"""
    
    def test_verify_email(self, api_client, admin_authenticated_client):
        """Test email verification process"""
        # First, register a new user
        reg_url = reverse('user-register')
        reg_response = admin_authenticated_client.post(reg_url, {
            'username': 'verifyuser',
            'email': 'verify@example.com',
            'password': 'Verify@123',
            'password2': 'Verify@123'
        }, format='json')
        
        # Get the verification token
        user = CustomUser.objects.get(username='verifyuser')
        token = user.email_verification_token
        
        # Verify the email
        verify_url = reverse('verify-email')
        verify_response = api_client.post(verify_url, {
            'token': token
        }, format='json')
        
        assert verify_response.status_code == status.HTTP_200_OK
        
        # Check that the user is now verified
        user.refresh_from_db()
        assert user.is_verified
        assert user.email_verification_token is None
        
        # Check that verification was logged
        assert UserActivity.objects.filter(
            user=user, 
            activity_type='email_verification'
        ).exists()
    
    def test_invalid_verification_token(self, api_client):
        """Test that invalid verification tokens are rejected"""
        verify_url = reverse('verify-email')
        verify_response = api_client.post(verify_url, {
            'token': 'invalid-token'
        }, format='json')
        
        assert verify_response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestPasswordReset:
    """Test password reset functionality"""
    
    def test_password_reset_request(self, api_client, regular_user):
        """Test password reset request process"""
        url = reverse('reset-password-request')
        response = api_client.post(url, {
            'email': regular_user.email
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that a token was generated
        regular_user.refresh_from_db()
        assert regular_user.password_reset_token is not None
        
        # Check that the request was logged
        assert UserActivity.objects.filter(
            user=regular_user, 
            activity_type='password_reset_request'
        ).exists()
    
    def test_password_reset_confirm(self, api_client, regular_user):
        """Test password reset confirmation process"""
        # First, set a reset token
        token = get_random_string(32)
        regular_user.password_reset_token = token
        regular_user.save()
        
        # Now use the token to reset the password
        url = reverse('reset-password-confirm')
        response = api_client.post(url, {
            'token': token,
            'new_password': 'NewPassword@123'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that the token was cleared
        regular_user.refresh_from_db()
        assert regular_user.password_reset_token is None
        
        # Check that the password was changed (by trying to login)
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(login_url, {
            'username': regular_user.username,
            'password': 'NewPassword@123'
        }, format='json')
        
        assert login_response.status_code == status.HTTP_200_OK
        
        # Check that the reset was logged
        assert UserActivity.objects.filter(
            user=regular_user, 
            activity_type='password_reset'
        ).exists()
    
    def test_invalid_reset_token(self, api_client):
        """Test that invalid reset tokens are rejected"""
        url = reverse('reset-password-confirm')
        response = api_client.post(url, {
            'token': 'invalid-token',
            'new_password': 'NewPassword@123'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestTwoFactorAuthentication:
    """Test two-factor authentication functionality"""
    
    def test_setup_2fa(self, user_authenticated_client, regular_user):
        """Test 2FA setup process"""
        url = reverse('setup-2fa')
        response = user_authenticated_client.post(url, {
            'device_name': 'My Phone'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'secret' in response.data
        assert 'uri' in response.data
        
        # Check that a device was created
        assert TOTPDevice.objects.filter(user=regular_user).exists()
        device = TOTPDevice.objects.get(user=regular_user)
        assert not device.confirmed
    
    def test_verify_2fa(self, user_authenticated_client, regular_user):
        """Test 2FA verification process"""
        # First, create a device
        device = create_totp_device(regular_user, "Test Device")
        
        # Generate a valid token
        token = get_totp_token(device.key)
        
        # Verify the token
        url = reverse('verify-2fa')
        response = user_authenticated_client.post(url, {
            'token': str(token)
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that the device is now confirmed
        device.refresh_from_db()
        assert device.confirmed
        
        # Check that 2FA is enabled for the user
        regular_user.refresh_from_db()
        assert regular_user.two_factor_enabled
        
        # Check that enabling 2FA was logged
        assert UserActivity.objects.filter(
            user=regular_user, 
            activity_type='2fa_enabled'
        ).exists()
    
    def test_disable_2fa(self, user_authenticated_client, regular_user):
        """Test disabling 2FA"""
        # First, create and confirm a device
        device = create_totp_device(regular_user, "Test Device")
        device.confirmed = True
        device.save()
        
        # Enable 2FA for the user
        regular_user.two_factor_enabled = True
        regular_user.save()
        
        # Generate a valid token
        token = get_totp_token(device.key)
        
        # Disable 2FA
        url = reverse('disable-2fa')
        response = user_authenticated_client.post(url, {
            'token': str(token),
            'password': 'Test@123'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that 2FA is now disabled
        regular_user.refresh_from_db()
        assert not regular_user.two_factor_enabled
        
        # Check that the device was deleted
        assert not TOTPDevice.objects.filter(user=regular_user).exists()
        
        # Check that disabling 2FA was logged
        assert UserActivity.objects.filter(
            user=regular_user, 
            activity_type='2fa_disabled'
        ).exists()

@pytest.mark.django_db
class TestAccountDeactivation:
    """Test account deactivation functionality"""
    
    def test_admin_can_deactivate_account(self, admin_authenticated_client, regular_user):
        """Test that an admin can deactivate user accounts"""
        url = reverse('deactivate-account', kwargs={'pk': regular_user.id})
        response = admin_authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that the user is now inactive
        regular_user.refresh_from_db()
        assert not regular_user.is_active
        
        # Check that deactivation was logged
        assert UserActivity.objects.filter(
            user=regular_user, 
            activity_type='account_deletion'
        ).exists()
    
    def test_regular_user_cannot_deactivate_account(self, user_authenticated_client, admin_user):
        """Test that a regular user cannot deactivate accounts"""
        url = reverse('deactivate-account', kwargs={'pk': admin_user.id})
        response = user_authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Check that the admin is still active
        admin_user.refresh_from_db()
        assert admin_user.is_active