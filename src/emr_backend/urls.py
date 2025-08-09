
# emergency_system/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # ⬅️ include your users app
    path('api/emergency/', include('emergency.urls')),  # ✅ Add this
]
# path('api/', include('users.urls')),



