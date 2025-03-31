"""
Django database utilities for enhancing database operations.

This package provides various utilities for working with Django's ORM,
including base models, query optimization, routing, and more.
"""

from .base import BaseModel
from .slugs import generate_unique_slug
from .queries import bulk_create_with_history, optimize_database_queries
from .routers import DatabaseRouter

__all__ = [
    'BaseModel',
    'generate_unique_slug',
    'bulk_create_with_history',
    'optimize_database_queries',
    'DatabaseRouter',
]
