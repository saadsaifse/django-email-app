from anymail.message import AnymailMessage
import os
from rest_framework.response import Response
from .models import SentEmail, get_status_choices_name
from .serializer import SentEmailSerializer
from rest_framework.generics import GenericAPIView
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class SendEmailView(GenericAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    queryset = SentEmail.objects.all()
    serializer_class = SentEmailSerializer

    def post(self, request):
        sender = request.data.get('sender')
        recipients = request.data.get('recipients')  # Comma-separated list of recipient email addresses
        recipients = recipients.split(',')  # Split the string into a list
        subject = request.data.get('subject')
        body = request.data.get('body')
        attachments = request.data.get('attachments')
        scheduled_send_at = request.data.get('scheduled_send_at')

        sent_email = SentEmail(sender=sender, subject=subject, body=body, attachments=attachments)

        if scheduled_send_at:
            sent_email.scheduled_send_at = scheduled_send_at

        sent_email.recipients = ', '.join(recipients)
        print(request.user)
        sent_email.user = request.user
        sent_email.save()

        message = AnymailMessage(
            subject=subject,
            body=body,
            from_email=sender,
            to=recipients,
        )
        if attachments and attachments.size > 0:
            attachments.seek(0)
            message.attach(attachments.name, attachments.read(), attachments.content_type)

        message.send()

        anymail_status = message.anymail_status
        print(anymail_status)
        anymail_status.message_id

        sent_email.message_id = anymail_status.message_id
        status_iterator = iter(anymail_status.status)
        first_item = next(status_iterator)
        sent_email.status = get_status_choices_name(first_item)
        sent_email.save()

        return Response({'message': 'Email sent successfully', 'message_id': anymail_status.message_id}, status=status.HTTP_200_OK)


class EmailViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Viewset for sent emails."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SentEmailSerializer
    queryset = SentEmail.objects.all()

    # def get_queryset(self):
    #     """Retrieve emails sent by the authenticated user."""
    #     queryset = self.queryset
    #     return queryset.filter(
    #         user=self.request.user
    #     ).order_by('-id').distinct()

