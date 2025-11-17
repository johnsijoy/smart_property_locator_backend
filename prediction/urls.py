# prediction/urls.py
from django.urls import path
from .views import predict_price

urlpatterns = [
    # Endpoint for predicting property price
    path('predict/', predict_price, name='predict-price'),
]
