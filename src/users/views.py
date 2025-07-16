# users/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from users.models import CustomUser, DoctorProfile, PatientProfile
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users.serializers import DoctorProfileSerializer, PatientProfileSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response



#doctor signup api
@csrf_exempt
@require_http_methods(["POST"])
def signup_doctor(request):
    data = json.loads(request.body)
    try:
        # Check if username/email already exists
        if CustomUser.objects.filter(username=data['email']).exists():
            return JsonResponse({'message': 'Username already taken'}, status=400)
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
    

#patient signup api
@csrf_exempt
@require_http_methods(["POST"])
def signup_patient(request):
    data = json.loads(request.body)
    try:
        # Check if username/email already exists
        if CustomUser.objects.filter(username=data['email']).exists():
            return JsonResponse({'message': 'Username already taken'}, status=400)
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
    
#my old login veiw 
#@csrf_exempt
#@require_http_methods(["POST"])
#def login_user(request):
#    data = json.loads(request.body)
#    user = authenticate(username=data['email'], password=data['password'])
#    if user is not None:
#        login(request, user)
#        role = 'doctor' if user.is_doctor else 'patient' if user.is_patient else 'unknown'
#        return JsonResponse({'message': 'Login successful', 'role': role})
#    else:
#        return JsonResponse({'message': 'Invalid email or password'}, status=401)

#login user api
@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    try:
        # First, fetch the user by email
        user_obj = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return JsonResponse({'message': 'Invalid email or password'}, status=401)

    # Now authenticate using the username (which is stored as the email)
    user = authenticate(username=user_obj.username, password=password)

    if user is not None:
        login(request, user)
        role = 'doctor' if user.is_doctor else 'patient' if user.is_patient else 'unknown'
        return JsonResponse({'message': 'Login successful', 'role': role})
    else:
        return JsonResponse({'message': 'Invalid email or password'}, status=401)


#Django's default authentication method
#@csrf_exempt
#@login_required
#@require_http_methods(["GET"])
#def get_patient_profile(request):
#    user = request.user

#    if not user.is_patient:
#        return JsonResponse({'message': 'Unauthorized'}, status=403)

#    try:
#        patient = PatientProfile.objects.get(user=user)
#        return JsonResponse({
#            'name': user.first_name,
#            'email': user.email,
#            'gender': patient.gender,
#            'contact': patient.contact,
#            'dob': patient.dob.strftime('%Y-%m-%d'),
#            'address': patient.address,
#            'city': patient.city,
#            'state': patient.state,
#        })
#    except PatientProfile.DoesNotExist:
#        return JsonResponse({'message': 'Profile not found'}, status=404)

# DRF authentication method for patient profile manual version
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def patient_profile(request):
#    user = request.user
#    try:
#        profile = PatientProfile.objects.get(user=user)

       # data = {

        #    'name': user.first_name,
        #    'email': user.email,
        
        #    'gender': profile.gender,
        
        #    'contact': profile.contact,
        #   'dob': profile.dob.strftime('%Y-%m-%d'),
        #    'address': profile.address,
         #   'city': profile.city,
         #   'state': profile.state,
        #}
        #return Response(data)
    
   # except PatientProfile.DoesNotExist:
    #    return Response({'error': 'Patient profile not found'}, status=404)

# DRF authentication method for doctors the manual version
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def doctor_profile(request):
#    user = request.user
#    try:
#        profile = DoctorProfile.objects.get(user=user)
#        data = {
#            'name': user.first_name,
 #           'email': user.email,
 #           'department': profile.department,
 #           'appointment': profile.appointment,
 #           'contact': profile.contact,
 #       }
 #       return Response(data)
 #   except DoctorProfile.DoesNotExist:
 #       return Response({'error': 'Doctor profile not found'}, status=404)

#Django's default authentication method
#@login_required
#def doctor_profile_api(request):
#    if not request.user.is_doctor:
#        return JsonResponse({'error': 'Unauthorized'}, status=403)

#    try:
#        doctor = DoctorProfile.objects.get(user=request.user)
#        return JsonResponse({
#            'name': request.user.first_name,
#            'email': request.user.email,
#            'department': doctor.department,
#            'appointment': doctor.appointment,
#            'contact': doctor.contact,
#            'gender': doctor.gender
#        })
#    except DoctorProfile.DoesNotExist:
#        return JsonResponse({'error': 'Doctor profile not found'}, status=404)




#@csrf_exempt
#@require_http_methods(["POST"])
#def logout_user(request):
#    if request.user.is_authenticated:
#        logout(request)
#        return JsonResponse({'message': 'Logout successful'})
#    return JsonResponse({'message': 'User not logged in'}, status=401)





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



# DRF logout version

#@csrf_exempt
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def logout_user(request):
#    logout(request)
#    return Response({'message': 'Logout successful'})



@csrf_exempt
@require_http_methods(["POST"])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    return JsonResponse({'message': 'User not logged in'}, status=401)