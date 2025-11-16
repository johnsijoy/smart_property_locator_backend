from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts
    path('api/accounts/', include('accounts.urls')),

    # Properties
    path('api/properties/', include('properties.urls')),

    # Price prediction endpoint
    path('api/predict-price/', include('prediction.urls')),
]

# ✅ Serve media files correctly during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
