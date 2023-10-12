from anymail.message import AnymailMessage
import os
from rest_framework.response import Response
from .models import SentEmail, get_status_choices_name
from .serializer import SentEmailSerializer, SentEmailStatusSerializer
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
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


class SendEmailView(GenericAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    queryset = SentEmail.objects.all()
    serializer_class = SentEmailSerializer

    def post(self, request):
        sender = request.data.get('sender')
        recipients = request.data.get('recipient')  # Comma-separated list of recipient email addresses
        recipients = [r.strip() for r in recipients.split(',')]  # Split the string into a list and trim
        subject = request.data.get('subject')
        body = request.data.get('body')
        attachment = request.data.get('attachment')
        scheduled_send_at = request.data.get('scheduled_send_at')

        sent_emails = []
        for r in recipients:
            sent_email = SentEmail(sender=sender, subject=subject, body=body, attachment=attachment, recipient=r)

            if scheduled_send_at:
                sent_email.scheduled_send_at = scheduled_send_at

            sent_email.user = request.user
            sent_email.recipient = r
            sent_email.save()
            sent_emails.append(sent_email)

        # Prepare to send emails to all recipients at once
        message = AnymailMessage(
            subject=subject,
            body=body,
            from_email=sender,
            to=recipients,
        )

        if attachment and attachment.size > 0:
            attachment.seek(0)
            message.attach(attachment.name, attachment.read(), attachment.content_type)

        message.send()
        anymail_status = message.anymail_status

        for email, recipient_status in anymail_status.recipients.items():
            sent_email = [se for se in sent_emails if se.recipient == email][0]
            sent_email.message_id = anymail_status.message_id
            sent_email.status = get_status_choices_name(recipient_status.status)
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


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'message_id',
                OpenApiTypes.STR,
                description='Message ID to filter',
            ),
            OpenApiParameter(
                'sender',
                OpenApiTypes.STR,
                description="Sender's email address to filter",
            ),
            OpenApiParameter(
                'recipient',
                OpenApiTypes.STR,
                description="Recipient's email address to filter",
            ),
        ]
    )
)
class EmailStatusViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SentEmailStatusSerializer

    def get_queryset(self):
        queryset = SentEmail.objects.all()

        # Apply filtering based on the query parameters
        message_id = self.request.query_params.get('message_id')
        sender = self.request.query_params.get('sender')
        recipient = self.request.query_params.get('recipient')

        if message_id:
            queryset = queryset.filter(message_id=message_id)
        if sender:
            queryset = queryset.filter(sender=sender)
        if recipient:
            queryset = queryset.filter(recipient=recipient)

        return queryset

