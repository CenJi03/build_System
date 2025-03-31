from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Allows for additional fields and customization
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        verbose_name=_('Unique Identifier')
    )
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Optional additional fields
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Resolve reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    def save(self, *args, **kwargs):
        """
        Override save method to ensure email is set
        """
        if not self.email:
            raise ValueError('Users must have an email address')
        
        # Convert email to lowercase to prevent duplicates
        self.email = self.email.lower()
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username
        
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class LoginAttempt(models.Model):
    """
    Model to track login attempts for security monitoring
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Login Attempts'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user or 'Unknown'} - {'Success' if self.successful else 'Failed'}"

class UserActivity(models.Model):
    """
    Model to track user activities for auditing purposes
    """
    ACTIVITY_TYPES = (
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('account_deletion', 'Account Deletion'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    additional_info = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"