# users/views.py

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from users.models import CustomUser, DoctorProfile, PatientProfile
from django.middleware.csrf import get_token 
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users.serializers import DoctorProfileSerializer, PatientProfileSerializer
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.shortcuts import render # You might need this import



#doctor signup api
@require_http_methods(["POST"])
def signup_doctor(request):
    data = json.loads(request.body)
    try:
        # Check if username/email already exists
       if CustomUser.objects.filter(email=data['email']).exists():
        return JsonResponse({'message': 'Email already in use'}, status=400)

        user = CustomUser.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['name']
        )
        user.is_doctor = True  # ✅ Add this
        user.save()
        
        DoctorProfile.objects.create(
            user=user,
            gender=data['gender'],
            department=data['department'],
            appointment=data['appointment'],
            contact=data['contact']
        )
        return JsonResponse({'message': 'Doctor signup successful'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
    
# csrf token initialization
def get_csrf_token(request):
    token = get_token(request)
    response = JsonResponse({'csrftoken': token})
    response.set_cookie('csrftoken', token, samesite='Lax') # Set the token as a cookie
    return response

#patient signup api
@require_http_methods(["POST"])
def signup_patient(request):
    data = json.loads(request.body)
    try:
        # Check if username/email already exists
        if CustomUser.objects.filter(email=data['email']).exists():
            return JsonResponse({'message': 'Email already in use'}, status=400)

        user = CustomUser.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['patient_name']
        )
        user.is_patient = True
        user.save()

        PatientProfile.objects.create(
            user=user,
            gender=data['gender'],
            contact=data['contact'],
            dob=data['dob'],
            address=data['address'],
            city=data['city'],
            state=data['state']
        )
        return JsonResponse({'message': 'Patient signup successful'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
    

# login user api
@require_http_methods(["POST"])
def login_user(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        role = 'doctor' if user.is_doctor else 'patient' if user.is_patient else 'unknown'
        return JsonResponse({'message': 'Login successful', 'role': role})
    else:
        return JsonResponse({'message': 'Invalid email or password'}, status=401)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_profile(request):
    user = request.user
    try:
        profile = DoctorProfile.objects.get(user=user)
        serializer = DoctorProfileSerializer(profile)
        return Response(serializer.data)
    except DoctorProfile.DoesNotExist:
        return Response({'error': 'Doctor profile not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_profile(request):
    user = request.user
    try:
        profile = PatientProfile.objects.get(user=user)
        serializer = PatientProfileSerializer(profile)
        return Response(serializer.data)
    except PatientProfile.DoesNotExist:
        return Response({'error': 'Patient profile not found'}, status=404)



@require_http_methods(["POST"])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    return JsonResponse({'message': 'User not logged in'}, status=401)