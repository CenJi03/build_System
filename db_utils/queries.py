from django.db import transaction
from typing import List, Type, Any, Optional


def bulk_create_with_history(model, objects, batch_size=None, ignore_conflicts=False):
    """
    Bulk create objects with option to create an audit trail
    
    :param model: Django model class
    :param objects: List of objects to create
    :param batch_size: Number of objects to create in each batch
    :param ignore_conflicts: Whether to ignore conflict errors
    :return: List of created objects
    """
    with transaction.atomic():
        created_objects = model.objects.bulk_create(
            objects, 
            batch_size=batch_size, 
            ignore_conflicts=ignore_conflicts
        )
        
        # Optional: Add audit logging or additional processing
        # You can extend this to log the bulk creation if needed
        
        return created_objects


def optimize_database_queries():
    """
    Provide recommendations for database query optimization
    
    This is a utility function to help developers identify 
    potential database performance improvements
    """
    recommendations = [
        "Use select_related() and prefetch_related() to reduce database queries",
        "Add database indexes to frequently queried fields",
        "Use values() or values_list() to retrieve only needed fields",
        "Avoid N+1 query problems by using joins and prefetching",
        "Use database-level filtering instead of Python-level filtering",
        "Consider using database-level aggregations",
        "Monitor and analyze slow queries"
    ]
    
    return recommendations


class QueryOptimizer:
    """
    A utility class to help optimize database queries by automatically
    applying commonly needed optimizations.
    """
    
    @staticmethod
    def select_only_needed_fields(queryset, fields):
        """
        Optimize a queryset to select only needed fields
        """
        return queryset.values(*fields)
    
    @staticmethod
    def prefetch_related_objects(queryset, *related_fields):
        """
        Automatically determine if prefetch_related or select_related should be used
        """
        from django.db import models
        
        select_related = []
        prefetch_related = []
        
        model = queryset.model
        for field_name in related_fields:
            try:
                field = model._meta.get_field(field_name.split('__')[0])
                if isinstance(field, models.ForeignKey) or isinstance(field, models.OneToOneField):
                    select_related.append(field_name)
                else:
                    prefetch_related.append(field_name)
            except:
                # If we can't determine the field type, default to prefetch_related
                prefetch_related.append(field_name)
        
        if select_related:
            queryset = queryset.select_related(*select_related)
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
            
        return queryset
