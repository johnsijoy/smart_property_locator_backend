from rest_framework import serializers
from .models import Property, Amenity, PropertyImage
from accounts.serializers import UserSerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image"]


class PropertySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Amenity.objects.all(),
        source='amenities',
        write_only=True,
        required=False
    )

    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = (
            "id", "owner",                 # <-- ADD OWNER HERE
            "title", "description",
            "property_type", "bhk", "area_sqft",
            "price", "location", "latitude", "longitude",
            "owner_name", "owner_email", "owner_phone",
            "amenities", "amenity_ids",
            "images",
            "created_at", "updated_at"
        )
        read_only_fields = ("id",)

    # --------------------------
    #       CREATE PROPERTY
    # --------------------------
    def create(self, validated_data):
        validated_data.pop("owner", None)

        lat = validated_data.get("latitude")
        lon = validated_data.get("longitude")
        if isinstance(lat, list):
            validated_data["latitude"] = lat[0]
        if isinstance(lon, list):
            validated_data["longitude"] = lon[0]

        request = self.context.get("request")
        amenities = validated_data.pop("amenities", [])

        property_obj = Property.objects.create(
            owner=request.user,
            **validated_data
        )

        if amenities:
            property_obj.amenities.set(amenities)

        images = request.FILES.getlist("images")
        for img in images:
            PropertyImage.objects.create(property=property_obj, image=img)

        return property_obj

    def update(self, instance, validated_data):
        validated_data.pop("owner", None)
        amenities = validated_data.pop("amenities", [])
        request = self.context.get("request")

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        if amenities:
            instance.amenities.set(amenities)

        new_images = request.FILES.getlist("images")
        for img in new_images:
            PropertyImage.objects.create(property=instance, image=img)

        return instance
