# CareDoor - Healthcare Management System

![Django](https://img.shields.io/badge/Django-4.2.2-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791)

## 📋 Overview

**CareDoor** is a comprehensive web-based Healthcare Management System developed as a Bachelor's Final Year Project (FYP). It streamlines healthcare operations by providing an integrated platform for managing appointments, patient records, prescriptions, and financial transactions in a healthcare facility.

The system supports multiple user roles with role-based access control, enabling seamless collaboration between patients, doctors, receptionists, and administrators.

## 🎯 Key Features

### 👥 Multi-Role User Management
- **Patients**: Browse specialists, book appointments, view prescriptions, communicate with doctors
- **Doctors**: Manage appointments, create prescriptions, view patient records, monitor availability
- **Receptionists**: Register patients, manage appointments, handle patient inquiries
- **Administrators**: Oversee all operations, manage staff, view financial reports

### 📅 Appointment Management
- Dynamic appointment slot availability based on doctor schedules
- Configurable working hours and days per doctor
- Real-time appointment status tracking
- Automatic appointment cancellation and completion workflows
- 30-minute appointment intervals (configurable)

### 💊 Prescription Management
- Doctors can create and update prescriptions for patients
- Complete prescription history tracking
- Patient access to medical records and prescriptions
- Timestamp tracking for created and updated prescriptions

### 💬 In-App Messaging
- Real-time messaging between patients and doctors
- Message delivery tracking
- Conversation history management
- Support for both synchronous and asynchronous communication

### 💰 Financial Management
- Automatic cashflow tracking for completed appointments
- Category-based fee management
- Revenue reports filtered by date
- Total earnings calculations

### 📊 Healthcare Categories
- Organized medical specializations (e.g., Cardiology, Dermatology, etc.)
- Category-specific fee structures
- Specialty-based doctor filtering for patients

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2.2
- **Language**: Python 3.10
- **Database**: PostgreSQL
- **Authentication**: Django's built-in authentication with custom User model

### Frontend
- **Markup**: HTML5
- **Styling**: CSS3 with custom stylesheets
- **Scripting**: JavaScript (ES6)
- **Templating**: Django Template Engine

### Key Libraries
- Django PostgreSQL support
- Django ArrayField for flexible data storage
- Pytz for timezone management
- Django Messages framework for user feedback

## 📦 Project Structure

```
CareDoor/
├── manage.py                 # Django management script
├── CareDoor/                 # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
│
├── caredoor_app/            # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic (1000+ lines of functionality)
│   ├── urls.py              # App-level URL routing
│   ├── forms.py             # Django forms
│   ├── managers.py          # Custom model managers
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   │
│   ├── templates/           # HTML templates
│   │   ├── admin/           # Admin role templates
│   │   ├── doctor/          # Doctor role templates
│   │   ├── patient/         # Patient role templates
│   │   └── *.html           # Shared templates
│   │
│   ├── static/              # Static files
│   │   ├── css/             # Stylesheets
│   │   ├── js/              # JavaScript files
│   │   └── images/          # Images and assets
│   │
│   └── migrations/          # Database migrations (33+ migrations)
│
└── venv/                    # Virtual environment
```

## 📊 Database Schema

### Core Models

#### User (Custom Authentication Model)
- Multi-role support (Patient, Doctor, Receptionist, Admin)
- Email-based authentication
- Profile information (name, age, gender, contact, address)
- Doctor-specific fields (specialization, working hours, availability schedule)

#### Appointment
- Links doctors and patients
- DateTime-based scheduling
- Status tracking (active/completed)
- Integrates with cashflow on completion

#### Prescription
- Doctor creates, patient accesses
- Stores medical details
- Tracks creation and update timestamps

#### Messages
- Patient-doctor communication
- Sender/receiver tracking
- Delivery timestamp logging

#### Categories
- Medical specializations
- Fee management per category
- Image support for visual representation

#### Cashflow
- Financial transaction recording
- Automatic creation on appointment completion
- Date-based financial reporting

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Virtual environment support

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/CareDoor.git
   cd CareDoor
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django==4.2.2
   pip install psycopg2-binary
   pip install pytz
   ```

4. **Configure Database**
   - Update `CareDoor/settings.py` with your PostgreSQL credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files** (for production)
   ```bash
   python manage.py collectstatic
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   
   Access the application at `http://localhost:8000`

## 🔐 User Roles & Access Control

### Patient
- **Landing Page**: Categories of medical specialists
- **Features**: 
  - Browse doctors by specialty
  - View available time slots
  - Book appointments
  - View prescriptions
  - Message doctors
  - Access appointment history

### Doctor
- **Dashboard**: List of scheduled appointments
- **Features**:
  - View daily/upcoming appointments
  - Access patient information
  - Create and update prescriptions
  - Mark appointments as completed
  - Manage working hours and availability
  - Communicate with patients

### Receptionist
- **Dashboard**: Appointment management interface
- **Features**:
  - Register new patients
  - View all appointments
  - Manage appointment records
  - Filter appointments by date/doctor

### Administrator
- **Dashboard**: Complete system oversight
- **Features**:
  - Register doctors and receptionists
  - Manage medical categories
  - View financial reports (cashflow)
  - Update staff information
  - System-wide user management

## 📱 Key Views & Functionality

### Authentication
- Login/Logout system with email-based authentication
- Role-based session management
- Signup for patient self-registration
- Custom user authentication backend

### Appointment Management
```python
- Check availability: Dynamic slot generation based on doctor's schedule
- Book appointment: Patient-initiated appointment creation
- Cancel appointment: User-initiated cancellation
- Mark complete: Doctor marks appointment as done, triggers cashflow entry
```

### Messaging System
- Real-time message exchange
- Asynchronous message retrieval via AJAX
- Message history management
- Delivery timestamp tracking

### Prescription Workflow
- Doctor-initiated prescription creation
- Patient view-only access
- Full prescription history tracking
- Update capability with timestamp management

### Financial Management
- Automatic fee charging based on specialization
- Cashflow report generation
- Date-range filtering for revenue analysis

## 🗄️ Database Migrations

The project includes 33 migrations tracking the evolution of the data model:
- Initial schema setup
- User model modifications (contact, profile enhancements)
- Appointment management improvements
- Prescription system implementation
- Financial tracking system
- Availability scheduling enhancements

## 🔧 Configuration

### Important Settings
- **Database**: PostgreSQL with Asia/Karachi timezone
- **Authentication**: Custom User model with email as USERNAME_FIELD
- **Static Files**: Django's static file handling with custom directories
- **Message Storage**: Session-based message storage
- **Debug Mode**: Currently enabled for development (disable for production)

### Security Considerations for Production
- [ ] Change `DEBUG = False` in settings
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for sensitive data (database credentials, SECRET_KEY)
- [ ] Implement HTTPS
- [ ] Use strong SECRET_KEY (change the insecure default)
- [ ] Configure CORS settings if building a separate frontend
- [ ] Implement rate limiting on authentication endpoints

## 🧪 Testing

The project includes a test file structure:
```bash
python manage.py test caredoor_app
```

## 📝 API Endpoints

### Authentication
- `GET /` - Login page
- `POST /` - Login submission
- `GET /signup/` - Patient signup page
- `POST /signup/` - Patient registration
- `GET /logout/` - Logout

### Appointment Management
- `GET /check-availability/<doctor_id>/` - View available slots
- `POST /book-slot/<doctor_id>/<start_time>/` - Book appointment
- `GET /my-appointments/` - Doctor's appointments
- `GET /appointmentlist/` - Receptionist view
- `POST /my-appointments/<id>/done/` - Mark complete
- `GET /my-appointments/<id>/cancel/` - Cancel appointment

### Prescription System
- `GET /patient-prescription/` - Patient's prescriptions
- `GET /doctor-prescription/` - Doctor's patient list
- `GET /doctor-prescription-page/<id>/` - Create/edit prescription

### Messaging
- `GET /messages/<receiver_id>/` - Message interface
- `POST /messages/<receiver_id>/` - Send message
- `GET /get_messages/<receiver_id>/` - Fetch messages (AJAX)

### User Profiles
- `GET /patient_profile/` - Patient dashboard
- `GET /doctor_profile/` - Doctor dashboard
- `GET /receptionist_profile/` - Receptionist dashboard

### Administrative
- `GET /dctor-form/` - Register doctor
- `GET /dctor-page2/` - Doctor list
- `GET /update-doctor/<id>/` - Update doctor
- `GET /recep-form/` - Register receptionist
- `GET /recep-page2/` - Receptionist list
- `GET /update-receptionist/<id>/` - Update receptionist
- `GET /patient-form/` - Patient list
- `GET /cashflow/` - Financial reports

## 🎨 Frontend Features

### Responsive Design
- CSS stylesheets for different user roles
- Print-friendly styles for prescriptions
- Mobile-friendly layout considerations

### Interactive Elements
- JavaScript-powered messaging (AJAX)
- Dynamic slot selection
- Form validation

### UI Components
- Role-specific navigation
- Appointment calendar/scheduler
- Prescription viewer
- Chat interface

## 🚨 Known Limitations & Future Enhancements

### Current Limitations
- Single-timezone support (Asia/Karachi)
- No real-time notifications
- Limited file upload capabilities
- No video consultation feature
- Single-page messaging (not live)

### Suggested Enhancements
- WebSocket integration for real-time messaging
- Email notifications for appointments
- SMS reminders using Twilio
- Video consultation integration (Jitsi/Zoom)
- Mobile app development (React Native/Flutter)
- Advanced prescription templates
- Medical record file uploads
- Analytics and reporting dashboard
- Integration with payment gateways (Stripe/PayPal)
- Multi-language support
- Doctor ratings and reviews

## 📚 Learning Outcomes

This project demonstrates proficiency in:

1. **Backend Development**
   - Django framework and MTV architecture
   - Custom user model implementation
   - Complex database relationships
   - Authentication and authorization
   - Session management

2. **Database Design**
   - Relational database modeling
   - PostgreSQL with Django ORM
   - Migration management
   - Query optimization

3. **Software Architecture**
   - Role-based access control (RBAC)
   - MVC/MTV design pattern
   - RESTful URL routing
   - Separation of concerns

4. **Frontend Integration**
   - Django templating
   - HTML/CSS/JavaScript integration
   - AJAX communication
   - Form handling

5. **Full-Stack Development**
   - End-to-end feature implementation
   - Integration of multiple components
   - User experience considerations

## 🤝 Contributing

This is an academic project. If you're interested in contributing improvements or enhancements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request


## ✍️ Author

**Pearson** - Bachelor's Final Year Project (FYP)

For inquiries or questions about this project, please open an issue on GitHub.

## 🎓 Academic Information

- **Project Type**: Bachelor's Final Year Project (FYP)
- **Duration**: Academic Year (2024-2025)
- **Institution**: [Your University Name]
- **Program**: [Your Program Name]
- **Purpose**: Demonstration of full-stack web development skills for Master's program applications

## 🔗 Resources & Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Best Practices](https://docs.djangoproject.com/en/4.2/topics/db/models/best-practices/)
- [Security in Django](https://docs.djangoproject.com/en/4.2/topics/security/)

## 📞 Support

For technical support or questions:
- Create an issue in the GitHub repository
- Check existing documentation and discussions
- Review Django's official documentation

---

**Last Updated**: September 2023
**Version**: 0.9
