from enum import Enum
from django.db import models
from django.contrib.auth.models import User

def get_status_choices_name(status_string):
    for status_choice in StatusChoices:
        if status_string == status_choice.value:
            return status_choice.name
    return None

class StatusChoices(Enum):
    QUEUED = 'queued'
    SENT = 'sent'
    REJECTED = 'rejected'
    FAILED = 'failed'
    BOUNCED = 'bounced'
    DEFERRED = 'deferred'
    DELIVERED = 'delivered'
    AUTORESPONDED = 'autoresponded'
    OPENED = 'opened'
    CLICKED = 'clicked'
    COMPLAINED = 'complained'
    UNSUBSCRIBED = 'unsubscribed'
    SUBSCRIBED = 'subscribed'
    UNKNOWN = 'unknown'

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
    status = models.CharField(
        max_length=13,
        choices=[(choice.name, choice.value) for choice in StatusChoices],
        default=StatusChoices.UNKNOWN.name,
    )