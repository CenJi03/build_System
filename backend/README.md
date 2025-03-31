# Secure Authentication System

A robust, secure authentication and user management system built with Django REST Framework.

## Features

### User Authentication
- JWT token-based authentication
- Admin-only user registration
- Email verification
- Password reset functionality
- Two-factor authentication using TOTP (Time-based One-Time Passwords)

### Security
- Rate limiting for login attempts and password resets
- Password complexity enforcement
- Login attempt tracking
- User activity logging
- IP address tracking for security monitoring

### Admin Controls
- Admin-only account deactivation
- User activity monitoring
- Login attempt monitoring
- User verification status management

## Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis (optional, for caching)

### 1. Clone Repository
```bash
git clone <repository-url>
cd backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env.development` file in the project root based on the provided template.

### 5. Set Up PostgreSQL Database
```bash
# Create database and user
createdb myprojectdb
createuser -P myprojectuser
# Grant privileges
psql -d myprojectdb -c "GRANT ALL PRIVILEGES ON DATABASE myprojectdb TO myprojectuser;"
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## Docker Development Setup

### 1. Prerequisites
- Docker
- Docker Compose

### 2. Build and Run Containers
```bash
docker-compose up --build
```

### 3. Access Services
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Postgres Database: localhost:5432
- Redis Cache: localhost:6379

## API Documentation

An interactive API documentation is available at:
- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`

## Testing

### Run Tests
```bash
# In the backend directory
pytest
```

### Check Test Coverage
```bash
pytest --cov=. --cov-report=html
# View coverage report in htmlcov/index.html
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

## Production Deployment

### 1. Create `.env.production` File
Create a `.env.production` file based on the template provided in the repository. Update all values with secure credentials.

### 2. Security Settings
Ensure the following settings are configured for production:
- `DEBUG=False`
- Set secure `SECRET_KEY` and `SIMPLE_JWT_SIGNING_KEY`
- Configure HTTPS settings
- Set proper `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`

### 3. Email Configuration
Configure a production email backend like SendGrid or Amazon SES:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your_sendgrid_api_key
```

### 4. Build and Deploy Docker Images
```bash
docker-compose -f docker-compose.production.yml up -d
```

## Security Considerations

- **JWT Tokens**: Configure appropriate lifetimes for access and refresh tokens
- **CORS**: Only allow trusted domains in `CORS_ALLOWED_ORIGINS`
- **Password Policies**: Enforce strong password requirements
- **Rate Limiting**: Protect against brute force attacks
- **Two-Factor Auth**: Encourage or require 2FA for sensitive operations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests to ensure they pass
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.