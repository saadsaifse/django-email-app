from django.db import models
from django.contrib.auth.models import User


class EmailMessage(models.Model):
    """Email Message object."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    messageId = models.CharField(max_length=255)
    recipientEmail = models.CharField(max_length=255)

    def __str__(self):
        return f'Id: {self.id}, Recipient: {self.recipientEmail}'