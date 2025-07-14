from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    

    def __str__(self):
        return self.user.username

   

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    appointment = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, default='Male')  # or 'Female' or 'Other'
    
  

    def __str__(self):
        return self.user.username



