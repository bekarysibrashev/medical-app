from .models import *
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import DateInput

TIME_CHOICES = [
    ('09:00', '09:00'),
    ('10:00', '10:00'),
    ('11:00', '11:00'),
    ('12:00', '12:00'),
    ('14:00', '14:00'),
    ('15:00', '15:00'),
    ('16:00', '16:00'),
    ('17:00', '17:00'),
    ('18:00', '18:00'),
    ('19:00', '19:00'),
    # Добавьте остальные временные интервалы
]

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_time']

    appointment_time = forms.ChoiceField(choices=TIME_CHOICES, required=True)
    
    
class YourModelForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth']
        widgets = {
            'date_of_birth': AdminDateWidget(),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'phone_number', 'email']
        
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }
        