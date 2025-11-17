from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Contact

User = get_user_model()


# --- User Serializer (for showing user info, e.g., property owner) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


# --- Buyer Registration Serializer ---
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)  # username is now required

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Only buyers can register from frontend
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='buyer'
        )
        return user
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# --- Login Serializer (for admin and buyer) ---
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # use email instead of username
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)  # authenticate with email
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data