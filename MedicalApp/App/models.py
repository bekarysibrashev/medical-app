from django.db import models
from django.core.exceptions import ValidationError

class Specialization(models.Model):
    specialization = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.specialization

class Patient(models.Model):
    name = models.CharField(max_length=100)
    
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"


# Create your models here.
class Doctors(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE) 
    img = models.ImageField()
    info = models.TextField()
    class Meta:
            verbose_name = 'Доктор'
            verbose_name_plural = 'Доктора'

    def __str__(self):
        return self.name
    


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_time = models.TimeField()
    is_available = models.BooleanField(default=True) 
    
    def save(self, *args, **kwargs):
        # Проверяем, доступно ли выбранное время
        existing_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_time=self.appointment_time,
            is_available=False  # Проверяем только занятые времена
        )

        if existing_appointments.exists():
            raise ValidationError("This appointment time is already taken.")

        # Если время доступно, сохраняем запись
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} at {self.appointment_time}"
