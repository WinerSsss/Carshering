# TAKE&DRIVE 🚗

Modern car rental service platform with REST API, real-time updates, and comprehensive features.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Docker Deployment](#docker-deployment)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)

## ✨ Features

### Core Functionality
- 🚗 **Car Management**: Add, update, and manage personal vehicles
- 📝 **Offer System**: Create and manage rental offers
- 📅 **Booking System**: Rent cars with flexible timelines
- 👤 **User Profiles**: Comprehensive user management with avatars
- 🔐 **Authentication**: Secure login, registration, and password reset
- 📊 **Rent Panel**: Track active and historical rentals
- 📄 **PDF Reports**: Generate rental confirmation documents

### Modern Features (New!)
- 🔌 **REST API**: Full-featured RESTful API with filtering and pagination
- 📚 **API Documentation**: Interactive Swagger/ReDoc documentation
- 🔍 **Advanced Search**: Filter and sort cars/offers by multiple criteria
- 📦 **Caching**: Redis-based caching for improved performance
- ⚡ **Async Tasks**: Celery integration for background jobs
- 🌍 **Internationalization**: Multi-language support (EN/PL)
- 🔒 **Enhanced Security**: CSRF protection, rate limiting, secure headers
- 🐳 **Docker Support**: Complete containerization with docker-compose
- 📈 **Logging**: Comprehensive logging system
- 🧪 **Testing**: Extensive test coverage with pytest

## 🛠 Tech Stack

### Backend
- **Django 5.0.6** - Web framework
- **Django REST Framework 3.15** - API framework
- **Celery 5.4** - Async task queue
- **Redis 5.0** - Caching and message broker
- **SQLite/PostgreSQL** - Database

### Frontend
- **Bootstrap 5** - UI framework
- **Crispy Forms** - Form rendering
- **JavaScript** - Interactive features

### DevOps
- **Docker & Docker Compose** - Containerization
- **Gunicorn** - WSGI HTTP Server
- **Nginx** (recommended for production)

### Development Tools
- **pytest** - Testing framework
- **Black** - Code formatter
- **Flake8** - Linter
- **isort** - Import sorter

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Redis (for caching and Celery)
- Docker & Docker Compose (optional)

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/WinerSsss/Carshering.git
cd Carshering
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://127.0.0.1:6379/1
EMAIL_LOGIN=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

5. **Database setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

7. **Run development server**
```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Redis (if not running as service)
redis-server

# Terminal 3: Celery worker
celery -A Carshering worker -l info

# Terminal 4: Celery beat (for scheduled tasks)
celery -A Carshering beat -l info
```

Visit `http://localhost:8000` to access the application.

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access the API documentation:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### API Endpoints

#### Cars
- `GET /api/v1/cars/` - List all cars (with filtering, search, pagination)
- `POST /api/v1/cars/` - Create a new car (authenticated)
- `GET /api/v1/cars/{id}/` - Get car details
- `PUT/PATCH /api/v1/cars/{id}/` - Update car (owner only)
- `DELETE /api/v1/cars/{id}/` - Delete car (owner only)
- `GET /api/v1/cars/my_cars/` - Get current user's cars

#### Offers
- `GET /api/v1/offers/` - List all offers (with filtering, search, pagination)
- `POST /api/v1/offers/` - Create a new offer (authenticated)
- `GET /api/v1/offers/{id}/` - Get offer details
- `PUT/PATCH /api/v1/offers/{id}/` - Update offer (owner only)
- `DELETE /api/v1/offers/{id}/` - Delete offer (owner only)
- `GET /api/v1/offers/available/` - Get only available offers
- `GET /api/v1/offers/my_offers/` - Get current user's offers

#### Rents
- `GET /api/v1/rents/` - List user's rents (with filtering, pagination)
- `POST /api/v1/rents/` - Create a new rent (authenticated)
- `GET /api/v1/rents/{id}/` - Get rent details
- `PUT/PATCH /api/v1/rents/{id}/` - Update rent (renter only)
- `DELETE /api/v1/rents/{id}/` - Delete rent (renter only)
- `POST /api/v1/rents/{id}/close/` - Close a rent
- `GET /api/v1/rents/active/` - Get active rents
- `GET /api/v1/rents/history/` - Get rent history

### Filtering Examples

```bash
# Filter cars by brand and year
GET /api/v1/cars/?car_brand=Toyota&min_year=2020

# Filter offers by price range
GET /api/v1/offers/?min_price=30&max_price=60

# Search cars
GET /api/v1/cars/?search=Camry

# Order results
GET /api/v1/cars/?ordering=-date_of_prod

# Pagination
GET /api/v1/cars/?page=2&page_size=20
```

### Authentication

The API supports two authentication methods:

1. **Session Authentication** (for web interface)
2. **Token Authentication** (for API clients)

To obtain a token:
```bash
POST /api/auth/login/
{
  "username": "your_username",
  "password": "your_password"
}
```

Use the token in requests:
```bash
curl -H "Authorization: Token your-token-here" http://localhost:8000/api/v1/cars/
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and start services**
```bash
docker-compose up -d
```

This will start:
- Web application (Django)
- Redis (caching & message broker)
- Celery worker (background tasks)
- Celery beat (scheduled tasks)

2. **Run migrations**
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

3. **Access the application**
- Web: `http://localhost:8000`
- API: `http://localhost:8000/api/v1/`
- Admin: `http://localhost:8000/admin/`

### Using Docker (Standalone)

```bash
# Build image
docker build -t takedrive .

# Run container
docker run -p 8000:8000 --env-file .env takedrive
```

## 💻 Development

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

### Creating Translations

```bash
# Generate translation files
python manage.py makemessages -l pl

# Compile translations
python manage.py compilemessages
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=carservice --cov-report=html

# Run specific test file
pytest carservice/tests/test_api.py

# Run specific test
pytest carservice/tests/test_api.py::TestCarAPI::test_list_cars_unauthenticated
```

### Test Coverage

Current test coverage includes:
- ✅ API endpoints (CRUD operations)
- ✅ Authentication and permissions
- ✅ Filtering and search
- ✅ Pagination and ordering
- ✅ Model validators
- ✅ Form validation
- ✅ Business logic

## 📊 Project Structure

```
Carshering/
├── carservice/          # Main app
│   ├── api_views.py    # REST API views
│   ├── serializers.py  # DRF serializers
│   ├── models.py       # Database models
│   ├── views.py        # Web views
│   ├── forms.py        # Django forms
│   ├── tasks.py        # Celery tasks
│   └── tests/          # Test suite
├── Carshering/         # Project settings
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL configuration
│   ├── celery.py       # Celery configuration
│   └── wsgi.py         # WSGI configuration
├── users/              # User management app
├── payment/            # Payment integration
├── templates/          # HTML templates
├── static/             # Static files
├── locale/             # Translation files
├── docker-compose.yml  # Docker Compose config
├── Dockerfile          # Docker configuration
└── requirements.txt    # Python dependencies
```

## 🔧 Configuration

### Redis Configuration

For production, configure Redis with persistence:

```yaml
# docker-compose.yml
redis:
  image: redis:7-alpine
  command: redis-server --appendonly yes
  volumes:
    - redis_data:/data
```

### Celery Tasks

Scheduled tasks run automatically:
- **Hourly**: Update rent statuses
- **Daily (3 AM)**: Clean up expired sessions

### Security Settings

For production deployment:

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **WinerSsss** - *Initial work* - [GitHub](https://github.com/WinerSsss)

## 🙏 Acknowledgments

- Django community for excellent documentation
- Bootstrap team for the UI framework
- All contributors who have helped improve this project

## 📞 Support

For support, email your-email@example.com or open an issue on GitHub.

## 🗺️ Roadmap

### Completed ✅
- REST API implementation
- Advanced filtering and search
- Caching with Redis
- Celery integration
- Docker support
- API documentation
- Comprehensive testing
- Internationalization

### Planned 🚧
- [ ] Map integration for car locations
- [ ] Real-time notifications (WebSockets)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-currency support
- [ ] Review and rating system
- [ ] Insurance integration
- [ ] AI-powered price suggestions

---

Made with ❤️ by the TAKE&DRIVE team
