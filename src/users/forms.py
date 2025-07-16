from django import forms
from .models import CustomUser, PatientProfile, DoctorProfile
from django.contrib.auth.forms import AuthenticationForm

class PatientSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        exclude = ['user']

class DoctorSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        exclude = ['user']

class LoginForm(AuthenticationForm):
    pass
