# smart_property_locator/properties/urls.py

from django.urls import path
from .views import (
    AmenityListCreateView,
    AmenityDetailView,
    PropertyListCreateView,
    PropertyDetailView,
    admin_dashboard_stats
)

urlpatterns = [
    # -----------------------------------------------
    # AMENITIES
    # -----------------------------------------------
    path('amenities/', AmenityListCreateView.as_view(), name='amenity-list-create'),
    path('amenities/<int:pk>/', AmenityDetailView.as_view(), name='amenity-detail'),

    # -----------------------------------------------
    # PROPERTIES
    # -----------------------------------------------
    path('', PropertyListCreateView.as_view(), name='property-list-create'),   # GET all, POST new
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),   # GET one, PUT, DELETE

    # -----------------------------------------------
    # ADMIN DASHBOARD STATS
    # -----------------------------------------------
    path('admin/stats/', admin_dashboard_stats, name='admin-stats'),
]
