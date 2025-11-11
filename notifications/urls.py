from django.urls import path
from .views import TwilioWebhookView 

urlpatterns = [
    path('whatsapp/', TwilioWebhookView.as_view(), name='whatsapp_bot'),

    
]
