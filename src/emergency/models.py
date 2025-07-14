from django.db import models
from users.models import CustomUser, DoctorProfile, PatientProfile

# Create your models here.


class EmergencyRequest(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    hospital_name = models.CharField(max_length=255)
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return f"Emergency from {self.patient.user.first_name} at {self.hospital_name}"
