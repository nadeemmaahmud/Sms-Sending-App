from django.forms import ModelForm, Textarea
from django import forms
from .models import Sms, Contact

class SmsForm(ModelForm):
    recipient_phone = forms.CharField(
        label='Recipient Phone Number',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Eg. +8801234567890'}),
    )

    class Meta:
        model = Sms
        fields = ['recipient_phone', 'message']
        widgets = {
            'message': Textarea(attrs={'placeholder': 'Enter your message', 'rows': 4}),
        }
        

    def save(self, commit=True):
        sms = super().save(commit=False)

        phone = self.cleaned_data['recipient_phone']

        contact, created = Contact.objects.get_or_create(phone_number=phone)

        sms.recipient = contact
        if commit:
            sms.save()
        return sms
    