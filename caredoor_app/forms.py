from django import forms
from .models import Appointment

class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'datetime']