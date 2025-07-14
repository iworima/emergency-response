from django.shortcuts import render
from .models import EmergencyRequest
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from users.models import PatientProfile, DoctorProfile # ✅ Import this
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required




# Create your views here.


@csrf_exempt
@require_http_methods(["POST"])
def request_emergency(request):
    data = json.loads(request.body)
    user = request.user

    if not user.is_authenticated or not user.is_patient:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    patient_profile = PatientProfile.objects.get(user=user)
    EmergencyRequest.objects.create(
        patient=patient_profile,
        hospital_name=data['hospital'],
        location_lat=data['lat'],
        location_lng=data['lng']
    )
    return JsonResponse({'message': 'Emergency request sent!'})


#my old loginrequest
#@csrf_exempt
#@require_http_methods(["GET"])

#def get_emergency_requests(request):
#
#    if not request.user.is_authenticated or not request.user.is_doctor:
#        return JsonResponse({'error': 'Unauthorized'}, status=401)
#
#    requests = EmergencyRequest.objects.filter(is_responded=False)
#    data = [{
#        'patient': req.patient.user.first_name,
#       'lat': req.location_lat,
#        'lng': req.location_lng,
#        'hospital': req.hospital_name,

#        'timestamp': req.timestamp.isoformat()
#    } for req in requests]

#   return JsonResponse({'requests': data})


@login_required
def get_emergency_requests(request):
    if not request.user.is_doctor:
        return JsonResponse({'message': 'Unauthorized'}, status=403)

    requests = EmergencyRequest.objects.all().order_by('-timestamp')  # or filter if needed
    data = [
        {
            'patient': req.patient.user.first_name,
            'hospital': req.hospital_name,
            'lat': req.location_lat,   # ✅ corrected
            'lng': req.location_lng,   # ✅ corrected
            'time': req.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for req in requests
    ]
    return JsonResponse({'requests': data})



@csrf_exempt
@require_http_methods(["POST"])
def respond_to_emergency(request):
    import json
    data = json.loads(request.body)
    user = request.user

    if not user.is_authenticated or not user.is_doctor:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        doctor_profile = DoctorProfile.objects.get(user=user)

        # Find the matching emergency request (e.g., by patient name & coords)
        emergency = EmergencyRequest.objects.filter(
            patient__user__first_name=data['patient_name'],
            location_lat=data['lat'],
            location_lng=data['lng'],
            is_responded=False
        ).first()

        if not emergency:
            return JsonResponse({'error': 'No matching emergency request found'}, status=404)

        emergency.doctor = doctor_profile
        emergency.is_responded = True
        emergency.save()

        return JsonResponse({'message': 'Emergency accepted and marked as responded'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



