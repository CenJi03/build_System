from django.utils.text import slugify


def generate_unique_slug(model_instance, slugable_field_name, slug_field_name):
    """
    Generate a unique slug for a model instance
    
    :param model_instance: The model instance
    :param slugable_field_name: The field to use for generating the slug
    :param slug_field_name: The slug field name
    :return: A unique slug
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    ModelClass = model_instance.__class__

    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{extension}"
        extension += 1

    return unique_slug


class SluggedModelMixin:
    """
    Mixin to automatically generate a slug when a model is saved
    
    Usage:
        class Article(SluggedModelMixin, models.Model):
            title = models.CharField(max_length=100)
            slug = models.SlugField(unique=True)
            
            # Define which field to use for the slug
            slug_field_name = 'title'
    """
    
    def save(self, *args, **kwargs):
        if not hasattr(self, 'slug_field_name'):
            raise AttributeError(
                f"{self.__class__.__name__} must define slug_field_name attribute"
            )
            
        if not getattr(self, 'slug', None):
            slug_field = getattr(self, 'slug_field_name')
            slug_value = generate_unique_slug(self, slug_field, 'slug')
            setattr(self, 'slug', slug_value)
            
        super().save(*args, **kwargs)
