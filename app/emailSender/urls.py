from django.urls import path
from .views import SendEmailView

app_name = 'emailSender'

urlpatterns = [
    path('send', SendEmailView.as_view()),
]