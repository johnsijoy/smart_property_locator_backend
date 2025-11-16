from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
import joblib
import numpy as np

from .models import Property, Amenity
from .serializers import PropertySerializer, AmenitySerializer
from .permissions import IsAdminOrReadOnly
from accounts.models import User


# ---------------------------------------------------------
# 1. LIST ALL PROPERTIES (Public)
# ---------------------------------------------------------
class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all().order_by("-id")
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]


# ---------------------------------------------------------
# 2. CREATE + LIST PROPERTIES (Admin POST, Public GET)
# ---------------------------------------------------------
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by("-id")
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["property_type", "location", "owner"]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["price", "created_at"]

    def perform_create(self, serializer):
        """
        Creates property + auto-assigns owner (admin user).
        Image saving handled in serializer.create()
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


# ---------------------------------------------------------
# 3. PROPERTY DETAIL (View / Update / Delete)
# ---------------------------------------------------------
class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrReadOnly]


# ---------------------------------------------------------
# 4. AMENITIES MANAGEMENT (Admin Only)
# ---------------------------------------------------------
class AmenityListCreateView(generics.ListCreateAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminUser]


class AmenityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminUser]


# ---------------------------------------------------------
# 5. PRICE PREDICTION API (Public)
# ---------------------------------------------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def predict_price_api(request):
    try:
        data = request.data

        location = data.get("location")
        property_type = data.get("property_type")
        bhk = int(data.get("bhk"))
        area_sqft = float(data.get("area_sqft"))

        model = joblib.load("smart_property_locator/prediction/price_model.pkl")
        location_encoder = joblib.load("smart_property_locator/prediction/location_encoder.pkl")
        type_encoder = joblib.load("smart_property_locator/prediction/type_encoder.pkl")

        loc_encoded = location_encoder.transform([location])[0]
        type_encoded = type_encoder.transform([property_type])[0]

        features = np.array([[loc_encoded, type_encoded, bhk, area_sqft]])
        predicted_price = model.predict(features)[0]

        return Response({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# ---------------------------------------------------------
# 6. ADMIN DASHBOARD STATS (Admin Only)
# ---------------------------------------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_dashboard_stats(request):
    total_properties = Property.objects.count()

    booked_properties = Property.objects.filter(is_booked=True).count() if hasattr(Property, "is_booked") else 0
    unbooked_properties = total_properties - booked_properties

    total_users = User.objects.count()
    buyer_count = User.objects.filter(role="buyer").count()
    admin_count = User.objects.filter(role="admin").count()

    bookings_percentage = (
        (booked_properties / total_properties) * 100 if total_properties > 0 else 0
    )

    return Response({
        "total_properties": total_properties,
        "booked_properties": booked_properties,
        "unbooked_properties": unbooked_properties,
        "total_users": total_users,
        "buyer_count": buyer_count,
        "admin_count": admin_count,
        "bookings_percentage": round(bookings_percentage, 2),
    })
