import base64
import hmac
import struct
import time
import hashlib
import random
import string
from django.utils import timezone
from .models import TOTPDevice

def generate_totp_secret():
    """
    Generate a random base32 encoded secret for TOTP
    """
    chars = list(string.ascii_uppercase + '234567')
    secret = ''.join(random.choice(chars) for _ in range(16))
    return secret

def generate_totp_uri(username, secret, issuer="YourApp"):
    """
    Generate a TOTP URI for QR code generation
    """
    return f"otpauth://totp/{issuer}:{username}?secret={secret}&issuer={issuer}"

def get_hotp_token(secret, intervals_no):
    """
    Generate an HOTP token
    """
    # Convert the secret from base32 to bytes
    key = base64.b32decode(secret, True)
    
    # Convert intervals_no to bytes
    msg = struct.pack(">Q", intervals_no)
    
    # Generate HMAC-SHA1
    h = hmac.new(key, msg, hashlib.sha1).digest()
    
    # Generate a 4-byte string (Dynamic Truncation)
    o = h[19] & 15
    
    # Generate HOTP value
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    
    return h

def get_totp_token(secret, window=30):
    """
    Generate a TOTP token
    """
    # Get the intervals number (number of intervals since Unix epoch)
    intervals_no = int(time.time() / window)
    
    # Generate and return the token
    return get_hotp_token(secret, intervals_no)

def verify_totp_token(secret, token, window=30, tolerance=1):
    """
    Verify a TOTP token
    
    Args:
        secret: The shared secret
        token: The token to verify
        window: The time window in seconds (default 30)
        tolerance: The number of windows to check before and after the current one
    """
    token = int(token)
    
    # Current interval number
    intervals_no = int(time.time() / window)
    
    # Check tokens within the tolerance
    for i in range(-tolerance, tolerance + 1):
        if get_hotp_token(secret, intervals_no + i) == token:
            return True
            
    return False

def get_user_totp_device(user, confirmed=True):
    """
    Get a user's TOTP device
    
    Args:
        user: The user
        confirmed: Whether to only get confirmed devices
    """
    devices = TOTPDevice.objects.filter(user=user)
    
    if confirmed:
        devices = devices.filter(confirmed=True)
        
    return devices.first()

def create_totp_device(user, name="Default"):
    """
    Create a new TOTP device for a user
    
    Args:
        user: The user
        name: The name of the device
    """
    # Generate a new secret
    secret = generate_totp_secret()
    
    # Create and save the device
    device = TOTPDevice.objects.create(
        user=user,
        name=name,
        key=secret,
        confirmed=False
    )
    
    return device

def confirm_totp_device(device, token):
    """
    Confirm a TOTP device with a token
    
    Args:
        device: The TOTP device
        token: The TOTP token
    """
    if verify_totp_token(device.key, token):
        device.confirmed = True
        device.last_used = timezone.now()
        device.save()
        return True
    return False