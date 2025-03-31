from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from .models import LoginAttempt, UserActivity

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create additional user-related records on user creation
    """
    if created:
        # Generate email verification token
        instance.email_verification_token = get_random_string(length=32)
        instance.save()

        # Optional: Send verification email
        try:
            from django.core.mail import send_mail
            from django.conf import settings

            verification_link = f"{settings.FRONTEND_URL}/verify-email?token={instance.email_verification_token}"
            send_mail(
                'Verify Your Email',
                f'Click the link to verify your email: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log email sending failure
            print(f"Failed to send verification email: {e}")

@receiver(pre_save, sender=User)
def track_username_change(sender, instance, **kwargs):
    """
    Track username changes
    """
    try:
        old_instance = User.objects.get(pk=instance.pk)
        if old_instance.username != instance.username:
            UserActivity.objects.create(
                user=instance,
                activity_type='profile_update',
                additional_info={
                    'old_username': old_instance.username,
                    'new_username': instance.username
                }
            )
    except User.DoesNotExist:
        # This is a new user, no previous username to compare
        pass

def log_successful_login(sender, user, request, **kwargs):
    """
    Log successful login attempt
    """
    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Create login attempt record
    LoginAttempt.objects.create(
        user=user,
        ip_address=ip,
        successful=True
    )

    # Create user activity record
    UserActivity.objects.create(
        user=user,
        activity_type='login',
        ip_address=ip
    )

def log_failed_login(sender, credentials, **kwargs):
    """
    Log failed login attempt
    """
    # This method would typically be connected to a signal from the authentication backend
    # For demonstration, you'd need to implement this in your custom authentication backend
    LoginAttempt.objects.create(
        user=None,  # No user for failed login
        ip_address=None,  # You'd need to track this from the request
        successful=False
    )