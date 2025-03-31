# Django Database Utilities

A collection of utilities for Django database operations.

## Features

- **BaseModel**: Abstract base model with common fields like UUID, created_at, updated_at
- **SoftDeleteModel**: Extends BaseModel with soft deletion capabilities
- **SluggedModelMixin**: Automatically generate slugs for your models
- **Database Routers**: Configurable routers for different database setups
- **Query Optimization**: Tools for optimizing database queries
- **Bulk Operations**: Enhanced bulk create with audit history support

## Installation

Add this package to your project's Python path.

## Usage

### Base Models

```python
from db_utils.base import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

### Soft Delete Support

```python
from db_utils.base import SoftDeleteModel

class Article(SoftDeleteModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
# Later in your code
article = Article.objects.get(id=1)
article.delete()  # This will soft delete
# To permanently delete:
article.hard_delete()
```

### Automatic Slugs

```python
from db_utils.slugs import SluggedModelMixin
from django.db import models

class BlogPost(SluggedModelMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    
    # Define which field to use for the slug
    slug_field_name = 'title'
```

### Query Optimization

```python
from db_utils.queries import QueryOptimizer

# Optimizing an existing queryset
products = Product.objects.all()
products = QueryOptimizer.prefetch_related_objects(
    products, 'category', 'tags', 'manufacturer'
)

# Only select needed fields
products = QueryOptimizer.select_only_needed_fields(
    products, ['id', 'name', 'price']
)
```

### Bulk Operations

```python
from db_utils.queries import bulk_create_with_history

products = [Product(name=f"Product {i}", price=10.99) for i in range(100)]
created_products = bulk_create_with_history(Product, products, batch_size=20)
```

## License

MIT