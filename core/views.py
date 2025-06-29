from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import SmsForm
from twilio.rest import Client
import os

def send_sms(request):
    if request.method == 'POST':
        form = SmsForm(request.POST)
        if form.is_valid():
            sms = form.save()

            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                twilio_message = client.messages.create(
                    body=sms.message,
                    from_=os.environ.get('sender_id'),
                    to=sms.recipient.phone_number
                )

                sms.status = 'sent'
                sms.save()

                messages.success(request, 'SMS sent successfully!')
            except Exception as e:
                messages.error(request, f'Failed to send SMS: {e}')
                print("Twilio error:", e)

            return redirect('home')
        else:
            print("Form is invalid.")
            print(form.errors)
    else:
        form = SmsForm()

    return render(request, 'index.html', {'form': form})

