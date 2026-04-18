# CareDoor - Project Architecture & Design

## System Overview

CareDoor is built on a three-tier architecture:

```
┌─────────────────────────────────────────────────┐
│          Presentation Layer (Templates)         │
│  - HTML/CSS/JavaScript User Interfaces          │
│  - Role-specific dashboards                     │
│  - Forms and interactive elements               │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         Business Logic Layer (Views)            │
│  - Request handling                             │
│  - Authentication & authorization               │
│  - Business process implementation              │
│  - Response generation                          │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         Data Access Layer (Models/ORM)          │
│  - Database abstraction                         │
│  - Data validation                              │
│  - Relationships management                     │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│      Database Layer (PostgreSQL)                │
│  - Data persistence                             │
│  - Transaction management                       │
└─────────────────────────────────────────────────┘
```

## Design Patterns Used

### 1. Model-View-Template (MVT)
Django's standard pattern adapted for healthcare operations:

```
User Request → URL Router → View → Model/Database → Template → Response
```

**Example Flow - Booking Appointment**:
```
Patient clicks "Book Slot" 
    → URL: /book-slot/<doctor_id>/<start_time>/
    → View: book_slot() checks permissions
    → Model: Creates Appointment record
    → Database: Saves appointment
    → Redirect: Shows confirmation
```

### 2. Role-Based Access Control (RBAC)

```python
# Decorator-based permission checks
@user_passes_test(is_doctor)
def appointments(request):
    """Only doctors can access this view"""
    pass

@user_passes_test(is_patient)
def categories(request):
    """Only patients can access this view"""
    pass
```

### 3. Authentication with Custom User Model

```
Standard Django User Model ← Override → Custom User Model
                                          ├── Email as primary key
                                          ├── Role-based fields
                                          ├── Domain-specific fields
```

### 4. Manager Pattern

```python
class UserManager(BaseUserManager):
    """Custom manager with domain-specific queries"""
    
    def create_user(self):
        """Create regular user"""
        
    def create_superuser(self):
        """Create admin user"""
        
    def get_by_natural_key(self, email):
        """Lookup by email"""
```

## Database Schema Design

### Entity Relationship Diagram

```
┌─────────────────────────┐
│         User            │
├─────────────────────────┤
│ id (PK)                 │
│ email (Unique)          │
│ name                    │
│ age                     │
│ gender                  │
│ contact (Unique)        │
│ address                 │
│ user_type (FK)          │◄──────────┐
│ specialization (FK)────┐│           │
│ is_superuser            ││           │
│ check_in                ││           │
│ check_out               ││           │
│ weekdays (Array)        ││           │
└─────────────────────────┘│           │
          ▲                 │           │
          │                 │           │
      ┌───┴─────────────┐   │      ┌────┴──────────────┐
      │                 │   │      │   Categories      │
      │                 │   │      ├───────────────────┤
      │           ┌─────┴───┼─────►│ id (PK)           │
      │           │         │      │ name (Unique)     │
      │           │         │      │ image             │
┌─────┴─────┐ ┌──┴──────────┴───┐  │ fee               │
│Appointment│ │   Messages      │  └───────────────────┘
├───────────┤ ├─────────────────┤
│ id (PK)   │ │ id (PK)         │
│ doctor ───┼┼─ doctor (FK) ────┼──► User
│ patient ──┼─ sender (FK) ────┐│
│start_time │ receiver (FK)────┐│
│ status    │ message         ││
└───────────┘ delivered_at     │
              └────────────────┘
              
┌──────────────────┐      ┌──────────────────┐
│  Prescription    │      │   Cashflow       │
├──────────────────┤      ├──────────────────┤
│ id (PK)          │      │ id (PK)          │
│ doctor (FK) ────┬────┐  │ appointment_dt   │
│ patient (FK) ───┼────┬──┤ patient (name)   │
│ details         │    │  │ doctor (name)    │
│ created_at      │    │  │ charges          │
│ updated_at      │    │  └──────────────────┘
└──────────────────┘    │
                        └─ Related to
                           Appointment
```

## Key Design Decisions

### 1. Email as USERNAME_FIELD
**Decision**: Use email instead of username
**Rationale**:
- More intuitive for users
- Healthcare context uses email/phone
- Unique email per person
- Better for international systems

### 2. Custom User Model with AbstractBaseUser
**Decision**: Create custom User model extending AbstractBaseUser
**Rationale**:
- Full control over authentication
- Can use email as primary field
- Flexible for future extensions
- Industry best practice for Django

### 3. Role-Based Architecture
**Decision**: Single User model with role field
**Alternative Considered**: Separate models per role (PatientModel, DoctorModel)
**Rationale**:
- Reduced code duplication
- Simpler shared data model
- Easier permission management
- Flexible role transitions

### 4. TimeField for Working Hours
**Decision**: Separate check_in and check_out TimeFields
**Rationale**:
- Simple and efficient
- Supports flexible working hours
- Easy to query availability
- Supports varying schedules

### 5. ArrayField for Availability Days
**Decision**: PostgreSQL ArrayField for weekdays
**Rationale**:
- Compact representation
- Easy filtering by day
- Supports non-sequential days off
- PostgreSQL native support

## Request/Response Flow

### Authentication Flow
```
┌─────────────────────────────────────────────────┐
│  1. User submits credentials (email + password) │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  2. View receives POST request to login_view()  │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  3. authenticate(email, password) checks User   │
│     - Validates email exists                    │
│     - Checks password hash                      │
└────────────┬────────────────────────────────────┘
             │
             ├─ Success ──┐
             │            ▼
             │    ┌────────────────────────┐
             │    │ Set user session      │
             │    │ login(request, user)  │
             │    └────────┬───────────────┘
             │             │
             │             ▼
             │    ┌────────────────────────┐
             │    │ Redirect by role:      │
             │    │ - A → Admin dashboard  │
             │    │ - D → Doctor dashboard │
             │    │ - P → Patient homepage │
             │    │ - R → Receptionist     │
             │    └────────────────────────┘
             │
             ├─ Failure
             │    └──► Re-render login with error message
             
             ▼
```

### Appointment Booking Flow
```
┌──────────────────────────────────────┐
│ Patient visits /categories/          │
│ Selects specialization               │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ View: listofdoctors()                │
│ - Filters User by specialization     │
│ - Returns doctor list                │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Patient selects doctor               │
│ Visits /check-availability/<doc_id>/ │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ View: check_availability()           │
│ 1. Get doctor's weekday schedule     │
│ 2. Get doctor's check_in/check_out   │
│ 3. Generate 30-min time slots        │
│ 4. Query existing Appointments       │
│ 5. Mark slots as free/occupied       │
│ 6. Return available slots            │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Patient selects time slot            │
│ Clicks "Book Appointment"            │
│ POST /book-slot/<doc_id>/<time>/     │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ View: book_slot()                    │
│ 1. Validate time slot exists         │
│ 2. Create Appointment object         │
│ 3. Save to database                  │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Redirect to availability page        │
│ Show confirmation message            │
└──────────────────────────────────────┘
```

## Security Considerations

### Current Implementations
- **CSRF Protection**: Django middleware protects POST requests
- **Password Hashing**: Django's PBKDF2 algorithm
- **SQL Injection**: ORM prevents SQL injection
- **Session Security**: Session-based authentication

### Recommendations for Production

```python
# settings.py

# HTTPS/SSL
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Sessions
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# Headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'

# Content Security
SECURE_CONTENT_SECURITY_POLICY = {...}
```

## Performance Optimization

### Query Optimization
```python
# BAD: N+1 query problem
appointments = Appointment.objects.all()
for appt in appointments:
    print(appt.patient.name)  # Extra query per iteration

# GOOD: Use select_related/prefetch_related
appointments = Appointment.objects.prefetch_related('patient')
```

### Database Indexing
Recommended indexes:
- `User.email` (PRIMARY KEY)
- `User.contact` (UNIQUE)
- `Appointment.doctor_id` (FOREIGN KEY)
- `Appointment.patient_id` (FOREIGN KEY)
- `Messages.sender_id` (FOREIGN KEY)
- `Cashflow.appointment_datetime` (Range queries)

### Caching Strategy
```python
# Cache available slots (5 minutes)
from django.core.cache import cache

available_slots = cache.get(f'slots_{doctor_id}')
if not available_slots:
    available_slots = generate_slots(doctor_id)
    cache.set(f'slots_{doctor_id}', available_slots, 300)
```

## Testing Strategy

### Unit Tests
```python
# Test individual models and functions
class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        pass
```

### Integration Tests
```python
# Test views and workflows
class AppointmentBookingTests(TestCase):
    def test_patient_can_book_appointment(self):
        pass
```

### End-to-End Tests
```
Patient Registration → Login → Browse Doctors → Book Appointment → Confirmation
```

## Future Architecture Considerations

### Microservices Potential
- Appointment Service
- Prescription Service
- Messaging Service
- Billing Service

### API-First Design
```python
# Future REST API
GET /api/doctors/ - List doctors
POST /api/appointments/ - Book appointment
GET /api/prescriptions/ - Get prescriptions
```

### Real-Time Features
- WebSocket for live messaging
- SignalR for notifications
- Redis for caching

---

For more details, see the main README.md and SETUP.md files.
