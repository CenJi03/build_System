# Backend Setup Guide

## Local Development Setup

### 6. Run Migrations
```bash
python backend/manage.py makemigrations
python backend/manage.py migrate
```

### 7. Create Superuser
```bash
python backend/manage.py createsuperuser
```

### 8. Run Development Server
```bash
python backend/manage.py runserver
```

## Docker Development Setup

### 1. Prerequisites
- Docker
- Docker Compose

### 2. Build and Run Containers
```bash
docker-compose up --build
```

### 3. Accessing Services
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Postgres Database: localhost:5432

## Testing

### Run Tests
```bash
# In the backend directory
pytest
```

### Code Quality Checks
```bash
# Run flake8 for linting
flake8 .

# Run black for formatting
black .

# Run isort for import sorting
isort .
```

## Security Features

### Authentication
- JWT Token Authentication
- Two-Factor Authentication Support
- Email Verification
- Password Complexity Rules

### Logging and Monitoring
- User Activity Logging
- Login Attempt Tracking
- Suspicious Activity Alerts

## Deployment Considerations
- Set `DEBUG=False` in production
- Use a strong, unique `SECRET_KEY`
- Configure proper CORS settings
- Set up HTTPS
- Use environment-specific settings

## Technologies Used
- Django 4.2
- Django REST Framework
- Simple JWT
- PostgreSQL
- Docker

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/your-project](https://github.com/yourusername/your-project)