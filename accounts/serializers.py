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
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')  # include username
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Only buyers can register from frontend
        user = User.objects.create_user(
            username=validated_data.get('username'),  # use .get() to avoid KeyError
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
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        data['user'] = user
        return data
