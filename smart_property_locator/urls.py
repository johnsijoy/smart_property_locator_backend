# smart_property_locator/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# Root endpoint
def root_view(request):
    return JsonResponse({"message": "API is running!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_view),  # ✅ Root URL returns a JSON message
    path('api/accounts/', include('accounts.urls')),       # Accounts app endpoints
    path('api/properties/', include('properties.urls')),   # Properties app endpoints
    path('api/predict-price/', include('prediction.urls')), # Prediction endpoints
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
