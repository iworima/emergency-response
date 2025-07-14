# users/urls.py
from django.urls import path
from . import views
from .views import get_doctor_profile, get_patient_profile  # DRF versions

urlpatterns = [
    path('signup/doctor/', views.signup_doctor, name='signup_doctor'),
    path('signup/patient/', views.signup_patient, name='signup_patient'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # DRF-based authenticated profile endpoints
    path('api/doctor/profile/', get_doctor_profile, name='doctor_profile'),
    path('api/patient/profile/', get_patient_profile, name='patient_profile'),
]
