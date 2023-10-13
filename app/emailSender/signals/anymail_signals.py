from anymail.signals import tracking
from django.dispatch import receiver
from ..models import SentEmail, get_status_choices_name


@receiver(tracking)  # add weak=False if inside some other function/class
def handle_status_change(sender, event, esp_name, **kwargs):
    if event.event_type in ['autoresponded', 'opened', 'clicked',
                            'complained', 'unsubscribed', 'subscribed']:
        return
    try:
        print('Received webhook signal for an email status update.')
        sent_email = SentEmail.objects.get(message_id=event.message_id,
                                           recipient=event.recipient)
        sent_email.status = get_status_choices_name(event.event_type)
        sent_email.save()
        print(f'Updated status of message {event.message_id} and recipient \
              {event.recipient} to {sent_email.status}')
    except SentEmail.DoesNotExist:
        print('Message and recipient in the webhook not in records.')
        pass


# Can also be implemented
@receiver(tracking)
def handle_bounce(sender, event, esp_name, **kwargs):
    if event.event_type == 'bounced':
        print("Message %s to %s bounced" % (
            event.message_id, event.recipient))


@receiver(tracking)
def handle_click(sender, event, esp_name, **kwargs):
    if event.event_type == 'clicked':
        print("Recipient %s clicked url %s" % (
            event.recipient, event.click_url))