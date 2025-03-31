import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        verbose_name=_('Unique Identifier')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Creation Timestamp')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Last Updated Timestamp')
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'


class SoftDeleteModel(BaseModel):
    """
    Abstract model that implements soft deletion instead of permanently
    removing records from the database.
    """
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('Is Deleted'),
        help_text=_('Indicates if this object has been soft-deleted')
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Deletion Timestamp'),
        help_text=_('When this object was deleted')
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Override delete method to perform soft deletion
        """
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    
    def hard_delete(self, using=None, keep_parents=False):
        """
        Permanently delete the record from the database
        """
        return super().delete(using=using, keep_parents=keep_parents)
