from django.urls import path
from .views import SendEmailView, EmailViewSet, EmailStatusViewSet

app_name = 'emailSender'

urlpatterns = [
    path('send/', SendEmailView.as_view(), name="send"),
    path('emails/', EmailViewSet.as_view({'get': 'list'}), name="emails"),
    path('status/', EmailStatusViewSet.as_view({'get': 'list'}), name="status"),
]