from rest_framework import serializers
from .models import SentEmail

class SentEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentEmail
        fields = '__all__'
        read_only_fields = ['id', 'message_id']

    scheduled_send_at = serializers.DateTimeField(
    format="%Y-%m-%dT%H:%M:%S",
    input_formats=["%Y-%m-%dT%H:%M:%S"],
    help_text="Enter a date and time in ISO format (e.g., '2023-10-15T14:30:00').",
    required=False
    )