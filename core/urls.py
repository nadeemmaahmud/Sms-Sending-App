from django.urls import path
from .views import send_sms, receive_sms

urlpatterns = [
    path('', send_sms, name='home'),
    path('sms/receive/', receive_sms, name='receive'),
]
