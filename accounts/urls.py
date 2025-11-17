from django.urls import path

from .views import ContactUsView, ContactListView 





from .views import (

    LoginView, RegisterView, AdminLoginAPIView,

    AdminUserListCreateView, AdminUserDetailView, ReplyToContactView, DeleteContactView

)



urlpatterns = [

    path('login/', LoginView.as_view(), name='buyer-login'),

    path('register/', RegisterView.as_view(), name='register'),

    path('admin-login/', AdminLoginAPIView.as_view(), name='admin-login'),

     # admin user management

    path('users/', AdminUserListCreateView.as_view(), name='admin-users-list'),

    path('users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-users-detail'),

           path('contact/', ContactUsView.as_view(), name='contact-us'),

    path('contact/queries/', ContactListView.as_view(), name='contact-queries'),

     path('contact/<int:pk>/reply/', ReplyToContactView.as_view(), name='contact-reply'),

     path('contact/<int:pk>/delete/', DeleteContactView.as_view(), name='contact-delete'),



]