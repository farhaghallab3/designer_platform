# whatsappbot/urls.py
from django.urls import path
from . import views 
from .views import ChatBotAPIView

urlpatterns = [
    path('whatsapp/webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
    path('chatbot/', ChatBotAPIView.as_view(), name='chatbot'),
]
