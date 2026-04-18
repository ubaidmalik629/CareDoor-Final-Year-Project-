# Welcome to CareDoor 👋

Thank you for visiting the **CareDoor** Healthcare Management System repository!

## 🎯 Quick Navigation

- **[📖 Full Documentation](README.md)** - Complete project overview
- **[🚀 Getting Started](SETUP.md)** - Installation and setup guide
- **[🏗️ Architecture](ARCHITECTURE.md)** - Technical design and patterns
- **[📊 Project Details](PROJECT_DETAILS.md)** - Statistics and metrics
- **[🤝 Contributing](CONTRIBUTING.md)** - How to contribute

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/CareDoor.git
cd CareDoor

# Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Then visit: `http://localhost:8000`

## 📚 What is CareDoor?

CareDoor is a comprehensive Healthcare Management System built with Django that enables:

- **Patients** to browse specialists, book appointments, and access medical records
- **Doctors** to manage appointments, create prescriptions, and monitor their schedules
- **Receptionists** to handle patient registration and appointment management
- **Administrators** to oversee operations and generate financial reports

## 🌟 Key Features

✅ Multi-role user system with email-based authentication  
✅ Intelligent appointment booking with real-time availability  
✅ Prescription management and patient medical records  
✅ Real-time messaging between patients and doctors  
✅ Financial tracking and revenue reporting  
✅ Category-based medical specializations  
✅ Flexible doctor scheduling (working hours & days)  

## 🛠️ Technology Stack

- **Backend**: Django 4.2.2 with Python 3.10
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Architecture**: MVC/MTV Pattern with Custom Authentication

## 📊 Project Stats

- **40+** View functions
- **6** Database models  
- **33** Database migrations
- **1000+** Lines of backend code
- **10+** User interface pages
- **35+** URL routes

## 🎓 Academic Purpose

This project is a **Bachelor's Final Year Project (FYP)** created to demonstrate:
- Full-stack web development skills
- Database design and optimization
- Software architecture and design patterns
- Real-world problem-solving
- Professional coding practices

Perfect for master's program applications!

## 🔐 Authentication

Default login options after setup:
- **Admin**: Created via `createsuperuser` command
- **Patient**: Self-registration via `/signup/`
- **Doctor/Receptionist**: Admin-created accounts

## 📁 Project Structure

```
CareDoor/
├── README.md              # Full documentation
├── SETUP.md              # Installation guide
├── ARCHITECTURE.md       # Technical design
├── CONTRIBUTING.md       # Contribution guidelines
├── requirements.txt      # Python dependencies
├── .env.example         # Configuration template
│
├── CareDoor/            # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── caredoor_app/        # Main application
    ├── models.py        # Database models
    ├── views.py         # Business logic
    ├── forms.py         # Django forms
    ├── managers.py      # Custom managers
    ├── templates/       # HTML templates
    ├── static/          # CSS, JS, images
    └── migrations/      # Database migrations
```

## 🚀 Features by Role

### 👤 Patient
- Browse medical specialties
- View available doctors
- Check appointment availability
- Book appointments
- Manage prescription records
- Chat with doctors

### 👨‍⚕️ Doctor
- View scheduled appointments
- Create patient prescriptions
- Update medical records
- Manage working hours
- Set availability schedule
- Chat with patients

### 💼 Receptionist
- Register new patients
- Manage appointment schedule
- View patient information
- Update patient records

### 🔐 Administrator
- Register doctors and staff
- Manage medical categories
- View financial reports
- System-wide user management

## 🧪 Testing

The project includes test structure:
```bash
python manage.py test caredoor_app
```

## 📝 Code Examples

### Appointment Booking
```python
# Patient books an appointment
appointment = Appointment.objects.create(
    doctor_id=selected_doctor,
    patient_id=request.user.id,
    start_time=selected_time
)
```

### Doctor Availability
```python
# Get available slots for a doctor
available_slots = get_doctor_availability(
    doctor=doctor,
    date=selected_date
)
```

### Financial Tracking
```python
# Automatically create cashflow on appointment completion
Cashflow.objects.create(
    appointment_datetime=timezone.now(),
    patient=appointment.patient.name,
    doctor=appointment.doctor.name,
    charges=appointment.doctor.specialization.fee
)
```

## 🔒 Security Features

- **Django CSRF Protection**: Prevents cross-site attacks
- **Password Hashing**: PBKDF2 algorithm
- **SQL Injection Prevention**: ORM-based queries
- **Session Management**: Secure session handling
- **Role-Based Access Control**: Permission decorators

## 📈 Scalability

Recommended enhancements for larger deployments:
- Database indexing optimization
- Caching layer (Redis)
- Message queuing (Celery)
- WebSocket integration (real-time messaging)
- API versioning (REST)
- Load balancing

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report bugs
- How to suggest features
- Code style guidelines
- Pull request process

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Pearson**  
Bachelor's Final Year Project (FYP)  
For Master's Program Application

## 📞 Questions?

- 📖 Check the [documentation](README.md)
- 🚀 See the [setup guide](SETUP.md)
- 🏗️ Review the [architecture](ARCHITECTURE.md)
- 💬 Create an issue for discussions

## 🎯 Learning Outcomes

This project demonstrates expertise in:

✅ Django framework and MTV architecture  
✅ Custom user models and authentication  
✅ PostgreSQL database design  
✅ Role-based access control (RBAC)  
✅ REST-like URL routing  
✅ Template rendering and inheritance  
✅ Real-world feature implementation  
✅ Full-stack development  
✅ Professional code documentation  
✅ Version control with Git  

## 🔗 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Python.org](https://www.python.org/)

---

<div align="center">

**Made with ❤️ for learning and growth**

⭐ If you find this project useful, please consider starring it!

</div>
