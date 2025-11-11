# core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from designers.views import PackageViewSet, DesignerProfileViewSet
from orders.views import OrderViewSet
from notifications.views import TwilioWebhookView , whatsapp_webhook

router = routers.DefaultRouter()
router.register(r'packages', PackageViewSet, basename='packages')
router.register(r'designers', DesignerProfileViewSet, basename='designers')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # Payments
    path('api/payments/', include('payments.urls')),

    # Twilio (SMS + WhatsApp Bot)
    path('api/twilio/webhook/', TwilioWebhookView.as_view(), name='twilio-webhook'),
    path('whatsapp/', whatsapp_webhook, name='whatsapp_webhook'),
    path('api/notifications/', include('notifications.urls')),

    # Auth
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/jwt/', include('accounts.jwt_urls')),
    path('api/accounts/', include('accounts.urls')),
]
