from django.urls import path, include
from .views import SendEmailView, EmailViewSet

app_name = 'emailSender'

urlpatterns = [
    path('send/', SendEmailView.as_view()),
    path('emails/', EmailViewSet.as_view({'get':'list'})),
]