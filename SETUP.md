# CareDoor - Installation & Setup Guide

## Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip & virtualenv
- Git

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/CareDoor.git
cd CareDoor
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

### 5. Configure PostgreSQL Database

```bash
# Create database
sudo -u postgres psql
CREATE DATABASE caredoor1;
CREATE USER postgres WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE caredoor1 TO postgres;
\q
```

Or update `CareDoor/settings.py` with your credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 8. Load Initial Data (Optional)
If you have fixtures for categories:
```bash
python manage.py loaddata initial_data
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Access at: `http://localhost:8000`

## Default Test Accounts

After running `createsuperuser`, use those credentials to log in.

To create test accounts via Django shell:
```bash
python manage.py shell
```

```python
from caredoor_app.models import User, Categories

# Create a test patient
patient = User.objects.create_user(
    email='patient@test.com',
    password='testpass123',
    name='Test Patient',
    age=30,
    gender='M',
    contact='03001234567',
    address='123 Test Street',
    user_type='P'
)

# Create a test category
category = Categories.objects.create(
    name='Cardiology',
    image='cardiology.png',
    fee=2000
)

# Create a test doctor
doctor = User.objects.create_user(
    email='doctor@test.com',
    password='testpass123',
    name='Dr. Test Doctor',
    age=45,
    gender='M',
    contact='03009876543',
    address='Hospital Address',
    user_type='D',
    specialization=category,
    check_in='09:00:00',
    check_out='17:00:00',
    weekdays=[0, 1, 2, 3, 4]  # Monday to Friday
)

# Create a test receptionist
receptionist = User.objects.create_user(
    email='receptionist@test.com',
    password='testpass123',
    name='Test Receptionist',
    age=28,
    gender='F',
    contact='03005555555',
    address='Hospital Address',
    user_type='R'
)

exit()
```

## Common Issues & Solutions

### Issue: "psycopg2 installation failed"
**Solution:**
```bash
# Install PostgreSQL development files first
sudo apt-get install postgresql postgresql-contrib
pip install psycopg2-binary
```

### Issue: "Database connection error"
**Solution:**
- Verify PostgreSQL is running: `sudo service postgresql status`
- Check credentials in settings.py
- Ensure database exists: `psql -l`

### Issue: "Static files not loading"
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: "AttributeError: 'Manager' object has no attribute 'get_by_natural_key'"
**Solution:**
This was fixed in the managers.py file. Ensure you have:
```python
def get_by_natural_key(self, email):
    return self.get(email=email)
```

## Development Server Commands

```bash
# Run server on specific port
python manage.py runserver 8080

# Interactive Python shell with Django context
python manage.py shell

# Create migrations for model changes
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate

# Create a new app (if needed)
python manage.py startapp app_name

# Run tests
python manage.py test

# Create a data migration
python manage.py makemigrations --empty caredoor_app --name migration_name
```

## Directory Structure for Static Files

Ensure these directories exist:
```
caredoor_app/static/
├── css/
│   ├── adminstyle.css
│   ├── doctorstyle.css
│   ├── patientstyle.css
│   ├── receptionstyle.css
│   ├── presc.css
│   └── print_styles.css
├── js/
│   └── presc.js
└── images/
    └── login.avif
```

## Database Reset (Development Only)

⚠️ **Warning**: This deletes all data!

```bash
# Delete database
dropdb caredoor1

# Recreate database
createdb caredoor1

# Reapply migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

## Production Deployment

Before deploying, update `CareDoor/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = 'your-secure-random-key'

# Use environment variables:
import os
DEBUG = os.getenv('DEBUG', False)
SECRET_KEY = os.getenv('SECRET_KEY')
```

## Testing the Application

1. **Login Test**:
   - Navigate to `http://localhost:8000`
   - Log in with superuser credentials

2. **Patient Flow**:
   - Sign up as patient
   - Browse categories
   - View doctors
   - Check availability
   - Book appointment

3. **Doctor Flow**:
   - Log in as doctor
   - View appointments
   - Create prescription
   - Mark appointment complete

4. **Admin Flow**:
   - Access admin dashboard
   - Register doctors/receptionists
   - View financial reports

## Troubleshooting

### Check Python Version
```bash
python --version  # Should be 3.10+
```

### Verify Django Installation
```bash
python -c "import django; print(django.get_version())"
```

### Database Connection Test
```bash
python manage.py dbshell
# Should open psql prompt if connection succeeds
```

## Need Help?

- Check Django documentation: https://docs.djangoproject.com/
- PostgreSQL help: https://www.postgresql.org/docs/
- Create an issue on GitHub repository
