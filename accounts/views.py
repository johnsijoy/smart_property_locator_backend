# smart_property_locator/accounts/views.py
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Contact
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.generics import DestroyAPIView

# Serializers
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ContactSerializer

User = get_user_model()


# -----------------------------
# Contact APIs
# -----------------------------
class ContactUsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queries = Contact.objects.all().order_by('-id')
        serializer = ContactSerializer(queries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Query sent successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactListView(generics.ListAPIView):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]


class ReplyToContactView(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def update(self, request, *args, **kwargs):
        contact = self.get_object()
        reply_text = request.data.get('reply', '')
        contact.reply = reply_text
        contact.replied = True
        contact.save()

        # Send email automatically
        send_mail(
            subject="Reply to your query",
            message=f"Dear {contact.name},\n\n{reply_text}\n\nBest Regards,\nSmart Property Locator Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            fail_silently=False,
        )

        return Response({"message": "Reply sent successfully!"}, status=status.HTTP_200_OK)


class DeleteContactView(DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]


# -----------------------------
# Admin User APIs
# -----------------------------
class AdminUserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(email=email, password=password)

        if user is not None and user.is_staff:
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Admin login successful.",
                "role": "admin",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        else:
            return Response(
                {"success": False, "error": "Invalid credentials or unauthorized."},
                status=status.HTTP_401_UNAUTHORIZED
            )


# -----------------------------
# Buyer APIs
# -----------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Only allow buyers in this view
            if user.role != 'buyer':
                return Response(
                    {"detail": "Only buyers can log in here"},
                    status=status.HTTP_403_FORBIDDEN
                )

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Buyer login successful",
                "role": user.role,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,   # include username for frontend
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)