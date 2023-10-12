from rest_framework import serializers
from .models import SentEmail

class SentEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentEmail
        fields = '__all__'
        read_only_fields = ['message_id']
