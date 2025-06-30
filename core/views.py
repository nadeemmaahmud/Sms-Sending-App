from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from .forms import SmsForm
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from .models import Sms, Contact
import os

def send_sms(request):
    numbers = Contact.objects.all()
    history = Sms.objects.all().order_by('-sent_at')
    if request.method == 'POST':
        form = SmsForm(request.POST)
        if form.is_valid():
            sms = form.save(commit=False)
            sms.sender = settings.TWILIO_PHONE_NUMBER

            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                twilio_message = client.messages.create(
                    body=sms.message,
                    from_=os.environ.get('TWILIO_PHONE_NUMBER'),
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

    return render(request, 'index.html', {'form': form, 'numbers': numbers, 'history': history})

@csrf_exempt
def receive_sms(request):
    if request.method == 'POST':
        from_number = request.POST.get('From')
        message_body = request.POST.get('Body')

        if not from_number or not message_body:
            return HttpResponse("Missing sender or message", status=400)

        sender_contact, created = Contact.objects.get_or_create(phone_number=from_number)
        recipient_contact, _ = Contact.objects.get_or_create(phone_number=settings.TWILIO_PHONE_NUMBER)

        Sms.objects.create(
            sender=from_number,
            recipient=recipient_contact,
            message=message_body,
            status='received',
        )

        response = MessagingResponse()
        response.message("Thanks! We received your message.")

        return HttpResponse(str(response), content_type='text/xml')

    return HttpResponse("Only POST requests allowed.", status=405)