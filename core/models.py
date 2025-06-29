from django.db import models
import os

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.phone_number

class Sms(models.Model):
    sender = models.CharField(max_length=25)
    recipient = models.ForeignKey(Contact, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('sent', 'Sent'),
    ], default='pending')

    def __str__(self):
        return f"From: {os.environ.get('sender_id')} To: {self.recipient} | Status: {self.status}"