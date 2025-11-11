from django.urls import path
from .views import CreateTabbyPaymentView, PaymentWebhookView

urlpatterns = [
    path('tabby/<int:order_id>/', CreateTabbyPaymentView.as_view(), name='tabby_payment'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment_webhook'),
]
