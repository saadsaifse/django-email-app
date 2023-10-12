from anymail.signals import tracking
from django.dispatch import receiver

@receiver(tracking)  # add weak=False if inside some other function/class
def handle_all(sender, event, esp_name, **kwargs):
        print("Message %s status updated to %s" % (
            event.message_id, event.event_type))

# Can be implemented
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