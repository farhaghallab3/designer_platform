# core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from designers.views import PackageViewSet, DesignerProfileViewSet
from orders.views import OrderViewSet
from payments.views import CreateCheckoutSession, StripeWebhook
from notifications.views import TwilioWebhookView

router = routers.DefaultRouter()
router.register(r'packages', PackageViewSet, basename='packages')
router.register(r'designers', DesignerProfileViewSet, basename='designers')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # Payment + Twilio webhooks
    path('api/payments/create-checkout-session/', CreateCheckoutSession.as_view(), name='create-checkout'),
    path('api/payments/webhook/', StripeWebhook.as_view(), name='stripe-webhook'),
    path('api/twilio/webhook/', TwilioWebhookView.as_view(), name='twilio-webhook'),

    # Auth endpoints
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/jwt/', include('accounts.jwt_urls')),

    # 👇 Add this line for your custom register/login/profile APIs
    path('api/accounts/', include('accounts.urls')),
]
