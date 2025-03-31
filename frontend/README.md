# Django Vue Authentication Project

## Overview

This is a full-stack web application demonstrating user authentication using Django (Backend) and Vue.js (Frontend) with JWT token-based authentication.

## Features

### Backend (Django)
- User Registration
- User Login/Logout
- JWT Token Authentication
- Profile Management
- Password Reset
- Email Verification
- Account Deletion
- Security Features
  - Password Hashing
  - Rate Limiting
  - CSRF Protection
  - Two-Factor Authentication Support

### Frontend (Vue.js)
- Responsive Authentication Forms
- State Management with Pinia
- Protected Routes
- Profile Editing
- Account Management
- Form Validation
- Error Handling

## Technology Stack

### Backend
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Simple JWT

### Frontend
- Vue 3
- Pinia
- Vue Router
- Axios
- Vite

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL
- Docker (optional)

## Local Development Setup

### Backend Setup

1. Navigate to backend directory
```bash
cd backend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
- Create `.env` file with necessary configurations
- Configure database settings

5. Run migrations
```bash
python manage.py migrate
```

6. Start development server
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to frontend directory
```bash
cd frontend
```

2. Install dependencies
```bash
npm install
```

3. Start development server
```bash
npm run dev
```

### Docker Deployment

1. Ensure Docker and Docker Compose are installed

2. Build and run services
```bash
docker-compose up --build
```

## Environment Variables

### Backend (.env)
- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

### Frontend (.env.development)
- `VITE_API_BASE_URL`

## Testing

### Backend Tests
```bash
python -m pytest
```

### Frontend Tests
```bash
npm run test
```

## Production Deployment

- Configure NGINX
- Use Gunicorn for Django
- Set up PostgreSQL
- Configure environment variables
- Use HTTPS
- Implement proper security measures

## Security Considerations

- Use strong, unique passwords
- Enable two-factor authentication
- Regularly update dependencies
- Use HTTPS
- Implement proper error handling

## License

[Specify your license]

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request