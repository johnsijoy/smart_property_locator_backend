# accounts/urls.py
from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    AdminLoginAPIView,
    AdminUserListCreateView,
    AdminUserDetailView,
    ContactUsView,
    ContactListView,
    ReplyToContactView,
    DeleteContactView
)

urlpatterns = [
    # Buyer authentication
    path('login/', LoginView.as_view(), name='buyer-login'),
    path('register/', RegisterView.as_view(), name='register'),

    # Admin authentication
    path('admin-login/', AdminLoginAPIView.as_view(), name='admin-login'),

    # Admin user management
    path('users/', AdminUserListCreateView.as_view(), name='admin-users-list'),
    path('users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-users-detail'),

    # Contact management
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('contact/queries/', ContactListView.as_view(), name='contact-queries'),
    path('contact/<int:pk>/reply/', ReplyToContactView.as_view(), name='contact-reply'),
    path('contact/<int:pk>/delete/', DeleteContactView.as_view(), name='contact-delete'),
]
