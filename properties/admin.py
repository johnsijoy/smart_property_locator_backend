from django.contrib import admin
from .models import Property, Amenity

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'property_type', 'bhk', 'area_sqft', 'price')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Amenity)
