# payments/urls.py
from django.urls import path
from .views import CreateTabbyPaymentView, PaymentWebhookView, MockPaymentSuccessView

urlpatterns = [
    path('create/<int:order_id>/', CreateTabbyPaymentView.as_view(), name='create-payment'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
    path('mock-success/<str:transaction_id>/', MockPaymentSuccessView.as_view(), name='mock-payment-success'),
]