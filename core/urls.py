from django.urls import path
from .views import send_sms

urlpatterns = [
    path('', send_sms, name='home'),
]
