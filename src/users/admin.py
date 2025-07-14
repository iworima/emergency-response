from django.contrib import admin
from .models import CustomUser, DoctorProfile, PatientProfile



admin.site.register(CustomUser)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)


# emrbackendsuperuser is the name of my superuser for this project.