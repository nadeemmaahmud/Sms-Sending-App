from django.db import models
import os

class Sms(models.Model):
    sender_id = models.CharField(default=os.environ.get('sender_id'))
    to_number = models.CharField(max_length=25)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.to_number} | From: {self.sender_id}"