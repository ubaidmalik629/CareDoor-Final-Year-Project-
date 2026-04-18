# Contributing to CareDoor

Thank you for considering contributing to the CareDoor Healthcare Management System!

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. **Check existing issues** - Avoid duplicates
2. **Provide detailed information**:
   - Python and Django version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Error traceback

**Example Issue Title**: 
`[BUG] Appointment booking fails for doctors with no availability`

### Suggesting Enhancements

1. **Describe the use case**
2. **Explain the expected benefit**
3. **Provide mockups or examples if possible**

**Example Issue Title**: 
`[FEATURE] Add email notifications for appointment reminders`

### Code Contributions

#### Setting Up Development Environment

```bash
git clone https://github.com/yourusername/CareDoor.git
cd CareDoor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow coding standards**
   - Use PEP 8 style guide
   - Write meaningful commit messages
   - Keep functions small and focused
   - Add docstrings to functions

3. **Write/Update Tests**
   ```bash
   python manage.py test caredoor_app
   ```

4. **Update Documentation**
   - Update README.md if adding features
   - Document API changes
   - Add inline code comments for complex logic

#### Commit Message Format

```
[TYPE] Brief description

Detailed explanation of what changed and why.
Reference related issues: Fixes #123, Related to #456
```

**Types**: 
- `[FEAT]` - New feature
- `[FIX]` - Bug fix
- `[DOCS]` - Documentation
- `[STYLE]` - Code style changes
- `[REFACTOR]` - Code refactoring
- `[TEST]` - Test additions/updates
- `[PERF]` - Performance improvements

#### Example Commit
```
[FEAT] Add email notifications for appointment reminders

- Implemented email notification system using Django signals
- Created notification templates for appointment confirmations
- Added settings for enabling/disabling notifications
- Includes 5 new unit tests

Fixes #42
```

### Pull Request Process

1. **Update your branch with latest main**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request** with:
   - Clear title and description
   - References to related issues
   - Screenshots for UI changes
   - Testing instructions
   - Checklist of changes

4. **Respond to Code Review**
   - Address feedback promptly
   - Ask questions if unclear
   - Push additional commits for changes

### Code Style Guidelines

#### Python (PEP 8)
```python
# Good
def calculate_appointment_duration(start_time, end_time):
    """Calculate duration between two datetime objects."""
    duration = end_time - start_time
    return duration.total_seconds() / 60

# Avoid
def calc_dur(st, et):
    d = et - st
    return d.total_seconds() / 60
```

#### Django Models
```python
class Appointment(models.Model):
    """Represents a scheduled appointment between doctor and patient."""
    
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_doctor',
        help_text='The doctor providing the appointment'
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_patient',
        help_text='The patient receiving the appointment'
    )
    start_time = models.DateTimeField(
        null=False,
        default=timezone.now,
        help_text='Appointment start date and time'
    )
    status = models.BooleanField(
        default=True,
        help_text='True if appointment is active, False if completed/cancelled'
    )
    
    class Meta:
        db_table = 'appointment'
        ordering = ['-start_time']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
    
    def __str__(self):
        return f"Appointment: {self.patient.name} with {self.doctor.name}"
```

#### Django Views
```python
@login_required(login_url='login')
@user_passes_test(is_doctor, login_url='/')
def appointments(request):
    """
    Display list of appointments for authenticated doctor.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse with rendered template containing doctor's appointments
    """
    doctor_id = request.user.id
    appointments = Appointment.objects.filter(
        doctor_id=doctor_id,
        status=True
    ).prefetch_related('patient')
    
    context = {'appointments': appointments}
    return render(request, 'doctor/appointments.html', context)
```

### Testing Guidelines

```python
from django.test import TestCase
from caredoor_app.models import User, Appointment

class AppointmentTestCase(TestCase):
    """Test cases for Appointment model and views."""
    
    def setUp(self):
        """Set up test data."""
        self.doctor = User.objects.create_user(
            email='doctor@test.com',
            password='testpass123',
            name='Dr. Test',
            user_type='D'
        )
        self.patient = User.objects.create_user(
            email='patient@test.com',
            password='testpass123',
            name='Test Patient',
            user_type='P'
        )
    
    def test_appointment_creation(self):
        """Test that an appointment can be created."""
        appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient
        )
        self.assertEqual(appointment.status, True)
        self.assertEqual(appointment.doctor, self.doctor)
```

## Project Structure

When adding new features, maintain this structure:

```
caredoor_app/
├── models.py          # Add model definitions
├── views.py           # Add view functions
├── forms.py           # Add Django forms
├── managers.py        # Add custom managers
├── templates/
│   └── new_feature/   # Add feature templates
├── static/
│   ├── css/           # Add feature styles
│   └── js/            # Add feature scripts
└── tests.py           # Add tests for feature
```

## Documentation Standards

### Model Documentation
```python
class YourModel(models.Model):
    """Brief description of the model.
    
    This model represents...
    
    Attributes:
        field_name (FieldType): Description of field
    """
```

### View Documentation
```python
def your_view(request, param):
    """Brief description of what the view does.
    
    Args:
        request (HttpRequest): The HTTP request object
        param (type): Description of parameter
        
    Returns:
        HttpResponse: Rendered template with context
        
    Raises:
        Http404: When object doesn't exist
        PermissionDenied: When user lacks access
    """
```

## Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #(issue number)
Related to #(issue numbers)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Tests added/updated
```

## Review Process

1. **Automated Checks**
   - Code style validation
   - Test execution
   - Database migration check

2. **Code Review**
   - Architecture and design
   - Code quality
   - Security considerations
   - Documentation completeness

3. **Approval**
   - At least one maintainer approval
   - All checks passing
   - No merge conflicts

## Questions?

- Open a discussion in GitHub
- Contact project maintainers
- Check existing documentation

---

**Happy Contributing!** 🚀

Your contributions help make CareDoor better for everyone!
