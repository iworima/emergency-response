from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_emergency, name='request_emergency'),
    path('requests/', views.get_emergency_requests, name='get_emergency_requests'),
    path('respond/', views.respond_to_emergency, name='respond_to_emergency'),
]
