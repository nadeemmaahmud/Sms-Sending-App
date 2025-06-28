from django.shortcuts import render, redirect
from .forms import SmsForm
from django.contrib import messages
from twilio.rest import Client
from django.conf import settings
from .models import Sms
import os

def index(request):
    my_number = os.environ.get('sender_id')
    if request.method == 'POST':
        form = SmsForm(request.POST)
    
        if form.is_valid():
            sms = form.save(commit=False)
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            try:
                client.messages.create(
                    body=sms.message,
                    from_="Nadim",
                    to=sms.to_number
                )
                messages.success(request, f"SMS sent successfully to {sms.to_number}!")
                sms.save()
                return redirect('index')
            except Exception as e:
                messages.error(request, f"Failed to send SMS: {str(e)}")
    else:
        form = SmsForm()

    return render(request, 'index.html', {'form': form, 'my_number': my_number})

def history(request):
    sms_history = Sms.objects.all().order_by('created_at').reverse()
    return render(request, 'history.html', {'sms_history': sms_history})