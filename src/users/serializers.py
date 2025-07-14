# users/serializers.py

from rest_framework import serializers
from users.models import DoctorProfile, PatientProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class DoctorProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = DoctorProfile
        fields = ['name', 'email', 'department', 'appointment', 'contact']


class PatientProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = PatientProfile
        fields = [
            'name', 'email', 'gender', 'contact', 'dob',
            'address', 'city', 'state'
        ]
