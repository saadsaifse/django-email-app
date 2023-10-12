from anymail.message import AnymailMessage
from rest_framework import status
from rest_framework.response import Response
from .models import SentEmail
from .serializer import SentEmailSerializer
from rest_framework.generics import GenericAPIView


class SendEmailView(GenericAPIView):
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
        sent_email.save()

        message = AnymailMessage(
            subject=subject,
            body=body,
            from_email=sender,
            to=recipients,
        )
        if attachments:
            message.attach(attachments.name, attachments.read(), attachments.content_type)

        message_id = message.send()

        sent_email.message_id = message_id
        sent_email.save()

        return Response({'message': 'Email sent successfully', 'message_id': message_id}, status=status.HTTP_200_OK)
