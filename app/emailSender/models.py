from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class SentEmail(models.Model):
    """Sent Email object."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    ),
    sender = models.EmailField()
    recipients = models.CharField(max_length=1000)  # Storing email addresses as a comma-separated string
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachments = models.FileField(upload_to='email_attachments/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    message_id = models.CharField(max_length=255, blank=True, null=True) # message Id returned from the email service provider
    scheduled_send_at = models.DateTimeField(null=True, blank=True)