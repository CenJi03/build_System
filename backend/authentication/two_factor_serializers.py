from rest_framework import serializers
from django.conf import settings
import pyotp
from django.contrib.auth import get_user_model

User = get_user_model()

class TOTPSetupSerializer(serializers.Serializer):
    """
    Serializer for setting up TOTP-based 2FA
    """
    totp_secret = serializers.CharField(read_only=True)
    totp_uri = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        # Generate a new TOTP secret
        totp_secret = pyotp.random_base32()
        user = self.context['request'].user
        
        # Create provisioning URI for QR code
        totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
            name=user.email,
            issuer_name=settings.APP_NAME if hasattr(settings, 'APP_NAME') else 'MyApp'
        )
        
        return {
            'totp_secret': totp_secret,
            'totp_uri': totp_uri
        }

class TOTPVerifySerializer(serializers.Serializer):
    """
    Serializer for verifying TOTP code and enabling 2FA
    """
    totp_code = serializers.CharField(required=True)
    totp_secret = serializers.CharField(required=True)
    
    def validate(self, attrs):
        totp_code = attrs.get('totp_code')
        totp_secret = attrs.get('totp_secret')
        
        # Verify the TOTP code
        totp = pyotp.TOTP(totp_secret)
        if not totp.verify(totp_code):
            raise serializers.ValidationError("Invalid verification code")
        
        return attrs

class TOTPDisableSerializer(serializers.Serializer):
    """
    Serializer for disabling 2FA
    """
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password")
        return value