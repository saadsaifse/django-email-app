from django.apps import AppConfig


class EmailsenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emailSender'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from .signals import anymail_signals