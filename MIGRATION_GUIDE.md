# Migration Guide: Upgrading to TAKE&DRIVE v2.0

This guide will help you migrate from the old version to the modernized TAKE&DRIVE v2.0.

## 🔄 Overview of Changes

### Major Updates
- Django upgraded from 4.2.2 to 5.0.6
- Added Django REST Framework 3.15
- Implemented Redis caching
- Added Celery for async tasks
- Enhanced security features
- Improved Docker configuration
- Added comprehensive API documentation
- Implemented internationalization

## 📋 Pre-Migration Checklist

- [ ] Backup your database
- [ ] Backup your `.env` file
- [ ] Backup uploaded media files
- [ ] Note your current Python version
- [ ] Document any custom modifications

## 🚀 Migration Steps

### Step 1: Backup Current System

```bash
# Backup database
cp db.sqlite3 db.sqlite3.backup

# Backup media files
cp -r media media.backup

# Backup environment
cp .env .env.backup
```

### Step 2: Update Python Environment

```bash
# Deactivate current virtual environment
deactivate

# Remove old virtual environment
rm -rf venv

# Create new virtual environment with Python 3.11+
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install New Dependencies

```bash
# Install updated requirements
pip install -r requirements.txt
```

### Step 4: Update Environment Variables

Update your `.env` file with new required variables:

```env
# Add these new variables to your existing .env

# CSRF Settings (NEW)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# CORS Settings (NEW)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Redis Configuration (NEW)
REDIS_URL=redis://127.0.0.1:6379/1

# Celery Configuration (NEW)
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Logging (NEW)
DJANGO_LOG_LEVEL=INFO
```

### Step 5: Install and Start Redis

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### On macOS:
```bash
brew install redis
brew services start redis
```

#### On Windows:
Download Redis from: https://github.com/microsoftarchive/redis/releases

Or use Docker:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

### Step 6: Run Database Migrations

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# If you encounter issues, try:
python manage.py migrate --run-syncdb
```

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 8: Create Logs Directory

```bash
mkdir -p logs
```

### Step 9: Test the Application

```bash
# Start Django development server
python manage.py runserver

# In another terminal, start Celery worker
celery -A Carshering worker -l info

# In another terminal, start Celery beat
celery -A Carshering beat -l info
```

### Step 10: Verify API Endpoints

Visit these URLs to verify everything works:

- Main site: http://localhost:8000
- API root: http://localhost:8000/api/v1/
- API docs: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

## 🔧 Breaking Changes

### 1. Settings Changes

**Old:**
```python
ALLOWED_HOSTS = ["*"]
```

**New:**
```python
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
```

### 2. URL Structure

New API endpoints have been added. Old web URLs remain unchanged:

**New API URLs:**
- `/api/v1/cars/` - Car API
- `/api/v1/offers/` - Offer API
- `/api/v1/rents/` - Rent API
- `/api/docs/` - API documentation

### 3. Task Execution

Tasks now run asynchronously via Celery:

**Old:**
```python
from carservice.tasks import update_status
update_status()  # Runs synchronously
```

**New:**
```python
from carservice.tasks import update_rent_statuses
update_rent_statuses.delay()  # Runs asynchronously
```

### 4. Caching

Views now use caching. To clear cache:

```python
from django.core.cache import cache
cache.clear()
```

## 🐳 Docker Migration

### Old Docker Setup

```bash
docker build -t takedrive .
docker run -p 8001:8001 takedrive
```

### New Docker Setup

```bash
# Using docker-compose (recommended)
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 🧪 Testing Migration

Run the test suite to ensure everything works:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=carservice

# Run specific test categories
pytest carservice/tests/test_api.py
pytest carservice/tests/test_models.py
```

## 🔍 Troubleshooting

### Issue: Redis Connection Error

**Error:** `redis.exceptions.ConnectionError: Error connecting to Redis`

**Solution:**
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start Redis
sudo systemctl start redis-server  # Linux
brew services start redis          # macOS
```

### Issue: Celery Not Starting

**Error:** `celery.exceptions.ImproperlyConfigured`

**Solution:**
```bash
# Ensure Redis is running
# Check CELERY_BROKER_URL in .env
# Try running with explicit broker URL
celery -A Carshering worker -l info --broker=redis://localhost:6379/0
```

### Issue: Migration Conflicts

**Error:** `django.db.migrations.exceptions.InconsistentMigrationHistory`

**Solution:**
```bash
# Option 1: Fake the migration
python manage.py migrate --fake carservice

# Option 2: Reset migrations (CAUTION: Development only)
python manage.py migrate carservice zero
python manage.py migrate carservice
```

### Issue: Static Files Not Loading

**Solution:**
```bash
# Collect static files again
python manage.py collectstatic --clear --noinput

# Check STATIC_ROOT in settings
# Ensure web server serves static files correctly
```

### Issue: Import Errors

**Error:** `ModuleNotFoundError: No module named 'rest_framework'`

**Solution:**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## 📊 Performance Optimization

### Enable Production Settings

Update `.env` for production:

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Configure Gunicorn

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 3 Carshering.wsgi:application
```

### Setup Nginx (Production)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/Carshering/staticfiles/;
    }

    location /media/ {
        alias /path/to/Carshering/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔐 Security Checklist

After migration, ensure:

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` is set
- [ ] `ALLOWED_HOSTS` is properly configured
- [ ] HTTPS is enabled (SSL certificate)
- [ ] Database credentials are secure
- [ ] Redis is password-protected (production)
- [ ] Firewall rules are configured
- [ ] Regular backups are scheduled

## 📝 Post-Migration Tasks

1. **Update Documentation**
   - Update any internal documentation
   - Inform team about new API endpoints

2. **Monitor Logs**
   ```bash
   tail -f logs/django.log
   ```

3. **Set Up Monitoring**
   - Configure error tracking (e.g., Sentry)
   - Set up uptime monitoring
   - Monitor Celery tasks

4. **Performance Testing**
   - Test API response times
   - Verify caching is working
   - Check database query performance

5. **User Communication**
   - Notify users of new features
   - Provide API documentation link
   - Update user guides

## 🆘 Rollback Procedure

If you need to rollback:

```bash
# Stop all services
docker-compose down  # If using Docker

# Restore database
cp db.sqlite3.backup db.sqlite3

# Restore media files
rm -rf media
cp -r media.backup media

# Restore environment
cp .env.backup .env

# Checkout previous version
git checkout previous-version-tag

# Reinstall old dependencies
pip install -r requirements.txt

# Restart services
python manage.py runserver
```

## 📞 Support

If you encounter issues during migration:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review logs in `logs/django.log`
3. Open an issue on GitHub
4. Contact support at your-email@example.com

## ✅ Migration Verification Checklist

- [ ] All dependencies installed successfully
- [ ] Redis is running and accessible
- [ ] Database migrations completed
- [ ] Static files collected
- [ ] Web interface loads correctly
- [ ] API endpoints respond correctly
- [ ] API documentation is accessible
- [ ] Celery worker is running
- [ ] Celery beat is running
- [ ] Scheduled tasks execute properly
- [ ] User authentication works
- [ ] File uploads work
- [ ] Email sending works (if configured)
- [ ] Tests pass successfully
- [ ] No errors in logs

## 🎉 Congratulations!

You've successfully migrated to TAKE&DRIVE v2.0! Enjoy the new features and improved performance.

For questions or feedback, please visit our [GitHub repository](https://github.com/WinerSsss/Carshering).