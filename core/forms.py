from django.forms import ModelForm, TextInput, Textarea
from .models import Sms

class SmsForm(ModelForm):
    class Meta:
        model = Sms
        fields = ['to_number', 'message']
        widgets = {
            'to_number': TextInput(attrs={'placeholder': '+8801xxxxxxxxx'}),
            'message': Textarea(attrs={'placeholder': 'Enter your message here', 'rows': 4}),
        }