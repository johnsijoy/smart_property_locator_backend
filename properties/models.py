from django.db import models
from django.conf import settings
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPES = (
        ('APARTMENT', 'Apartment'),
        ('HOUSE', 'House'),
        ('CONDO', 'Condo'),
        ('LAND', 'Land'),
        ('COMMERCIAL', 'Commercial'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    bhk = models.IntegerField(null=True, blank=True)
    area_sqft = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    amenities = models.ManyToManyField('Amenity', related_name='properties', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    owner_phone = models.CharField(max_length=20, blank=True, null=True)
    def save(self, *args, **kwargs):
        # Auto-update latitude and longitude if missing
        if self.location and (self.latitude is None or self.longitude is None):
            geolocator = Nominatim(user_agent="my_property_app", timeout=10)
            try:
                location = geolocator.geocode(self.location)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                else:
                    print(f"Warning: Could not geocode location '{self.location}'")
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(f"Geocoding error for '{self.location}': {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"
