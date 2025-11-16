import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from properties.models import Amenity, Property
from django.conf import settings

class Command(BaseCommand):
    help = 'Seeds the database with sample data (stores images as objects).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_superuser': True, 'is_staff': True}
        )
        if created:
            admin_user.set_password('adminpassword')
            admin_user.save()

        # Create amenities
        amenity_names = [
            'School', 'Hospital', 'Park', 'Bus Stop',
            'Gym', 'Shopping Mall', 'Restaurant', 'Metro Station'
        ]
        for name in amenity_names:
            Amenity.objects.get_or_create(name=name)
        amenities = list(Amenity.objects.all())

        # Property data with unique owners
        property_data = [
            {
                'title': 'HOUSE in Springfield',
                'location': '123 Maple St, Springfield, IL',
                'property_type': 'House',
                'images': ['/images/prop1.png', '/images/prop2.png'],
                'latitude': 39.78,
                'longitude': -89.64,
                'price': 600000,
                'bhk': 2,
                'owner': {'username': 'John', 'email': 'john@example.com', 'contact_no': '+1234567890'},
            },
            {
                'title': 'HOUSE in Capital City',
                'location': '45 Pine Ave, Capital City, CA',
                'property_type': 'House',
                'images': ['/images/prop3.png', '/images/prop4.png'],
                'latitude': 38.90,
                'longitude': -77.03,
                'price': 550000,
                'bhk': 3,
                'owner': {'username': 'Ria', 'email': 'ria@example.com', 'contact_no': '+1987456321'},
            },
            {
                'title': 'HOUSE in Rivertown',
                'location': '202 Birch Rd, Rivertown, TX',
                'property_type': 'House',
                'images': ['/images/prop5.png', '/images/prop6.png'],
                'latitude': 30.15,
                'longitude': -95.45,
                'price': 500000,
                'bhk': 4,
                'owner': {'username': 'Mia', 'email': 'mia@example.com', 'contact_no': '+1876456123'},
            },
            {
                'title': 'HOUSE in 202 Birch Rd',
                'location': '202 Birch Rd, Rivertown, TX',
                'property_type': 'House',
                'images': ['/images/prop7.png', '/images/prop8.png'],
                'latitude': 36.15,
                'longitude': -95.45,
                'price': 700000,
                'bhk': 4,
                'owner': {'username': 'Jess', 'email': 'jess@example.com', 'contact_no': '+1234098765'},
            },
            {
                'title': 'APARTMENT in 123 Maple St',
                'location': '123 Maple St, Springfield, IL',
                'property_type': 'Apartment',
                'images': ['/images/prop9.png', '/images/prop10.png'],
                'latitude': 30.15,
                'longitude': -95.45,
                'price': 400000,
                'bhk': 3,
                'owner': {'username': 'James', 'email': 'james@example.com', 'contact_no': '+1999888777'},
            },
            {
                'title': 'CONDO in 202 Birch Rd',
                'location': '202 Birch Rd, Rivertown, TX',
                'property_type': 'Condo',
                'images': ['/images/imagecopy.png', '/images/imagecopy8.png'],
                'latitude': 35.15,
                'longitude': -85.45,
                'price': 520000,
                'bhk': 3,
                'owner': {'username': 'Ava', 'email': 'ava@example.com', 'contact_no': '+1777888999'},
            },
            {
                'title': 'APARTMENT in 45 Pine Ave',
                'location': '45 Pine Ave, Capital City, CA',
                'property_type': 'Apartment',
                'images': ['/images/imagecopy2.png', '/images/imagecopy9.png'],
                'latitude': 33.15,
                'longitude': -95.45,
                'price': 430000,
                'bhk': 2,
                'owner': {'username': 'Liam', 'email': 'liam@example.com', 'contact_no': '+1666777888'},
            },
            {
                'title': 'APARTMENT in 101 Elm Blvd',
                'location': '101 Elm Blvd, Lakeside, FL',
                'property_type': 'Apartment',
                'images': ['/images/imagecopy3.png', '/images/imagecopy10.png'],
                'latitude': 30.15,
                'longitude': -95.45,
                'price': 310000,
                'bhk': 1,
                'owner': {'username': 'Sophia', 'email': 'sophia@example.com', 'contact_no': '+1555666777'},
            },
            {
                'title': 'CONDO in 123 Maple St',
                'location': '123 Maple St, Springfield, IL',
                'property_type': 'Condo',
                'images': ['/images/imagecopy4.png', '/images/imagecopy11.png'],
                'latitude': 35.25,
                'longitude': -95.45,
                'price': 600000,
                'bhk': 3,
                'owner': {'username': 'Noah', 'email': 'noah@example.com', 'contact_no': '+1444555666'},
            },
            {
                'title': 'CONDO in 101 Elm Blvd',
                'location': '101 Elm Blvd, Lakeside, FL',
                'property_type': 'Condo',
                'images': ['/images/imagecopy5.png', '/images/imagecopy12.png'],
                'latitude': 30.15,
                'longitude': -95.45,
                'price': 700000,
                'bhk': 2,
                'owner': {'username': 'Olivia', 'email': 'olivia@example.com', 'contact_no': '+1333444555'},
            },
        ]

        # Path to frontend images folder
        frontend_images_folder = os.path.join(settings.BASE_DIR, '../smart-property-locator-frontend/public/images')

        # Create properties
        for info in property_data:
            # Create or get owner
            owner_info = info['owner']
            owner_user, _ = User.objects.get_or_create(
                username=owner_info['username'],
                defaults={'email': owner_info['email']}
            )
            owner_user.set_password('ownerpassword')
            owner_user.save()

            # Check images exist
            images_obj = []
            for img_path in info['images']:
                full_path = os.path.join(frontend_images_folder, os.path.basename(img_path))
                if not os.path.exists(full_path):
                    self.stdout.write(self.style.WARNING(f"⚠️ Image not found: {full_path}"))
                images_obj.append({'image': img_path})

            # Create or update property
            prop, created = Property.objects.update_or_create(
                title=info['title'],
                defaults={
                    'owner': owner_user,
                    'description': f"A beautiful {info['property_type'].lower()} at {info['location']}.",
                    'price': info['price'],
                    'location': info['location'],
                    'latitude': info['latitude'],
                    'longitude': info['longitude'],
                    'property_type': info['property_type'],
                    'images': images_obj,
                }
            )

            # Set amenities
            prop.amenities.set(amenities)

            # Add BHK
            if hasattr(prop, 'bhk'):
                prop.bhk = info['bhk']
                prop.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created property: {prop.title}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"🔁 Updated property: {prop.title}"))

        self.stdout.write(self.style.SUCCESS('🎉 Seeding complete!'))
