from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
from caredoor_app.managers import UserManager
from django.utils import timezone
from datetime import datetime, timedelta, time

class Categories(models.Model):
    class Meta:
        db_table = 'categories'
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True)
    image = models.CharField()
    fee = models.IntegerField(default=1300)


class User(AbstractBaseUser):
    class Meta:
        db_table = "user"

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    USER_TYPES = (
        ("P", "Patient"),
        ("D", "Doctor"),
        ("A", "Admin"),
        ("R", "Receptionist"),
    )
    WEEKDAYS_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    name_validator = RegexValidator(
        r"^[A-Za-z ]+$", "Name can only contain letters and spaces."
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, validators=[name_validator])
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact = models.CharField(unique=True, max_length=11)
    address = models.TextField(max_length=255)
    specialization = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_id", null=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPES)
    is_superuser = models.BooleanField(default=False)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    weekdays = ArrayField(models.IntegerField(choices=WEEKDAYS_CHOICES), blank=True, null=True)

    USERNAME_FIELD = "email"

    objects = UserManager()
    
    def __str__(self):
        return self.email
    
class Appointment(models.Model):
    class Meta:
        db_table = 'appointment'

    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_id", null=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_id", null=False)
    start_time = models.DateTimeField(null=False, default=timezone.now)
    status = models.BooleanField(default=True)

    
class Messages(models.Model):
    class Meta:
        db_table  = 'messages'
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_id", null=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_id", null=False)
    message = models.CharField()
    delivered_at = models.DateTimeField(null=False, default=now)

class Prescription(models.Model):
    class Meta:
        db_table = 'prescription'

    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_doctor_id", null=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_patient_id", null=False)
    details = models.CharField(null=False)
    created_at = models.DateTimeField(null=False, default=now)
    updated_at = models.DateTimeField(null=False, default=now)

class Cashflow(models.Model):
    class Meta:
        db_table = 'cashflow'
    appointment_datetime = models.DateTimeField(null=False)
    patient = models.CharField(null=False, max_length=255)
    doctor = models.CharField(null=False, max_length=255)  
    charges = models.IntegerField(null=False)

