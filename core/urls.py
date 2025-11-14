# core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from designers.views import PackageViewSet, DesignerProfileViewSet
from orders.views import OrderViewSet
from notifications.views import TwilioWebhookView  

router = routers.DefaultRouter()
router.register(r'packages', PackageViewSet, basename='packages')
router.register(r'designers', DesignerProfileViewSet, basename='designers')  # This creates /api/designers/
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # This includes ALL router URLs
    
    # Remove this line - it's creating duplicate designers URLs
    # path('api/designers/', include('designers.urls')),
    
    # Other URLs
    path('api/', include('whatsappbot.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/twilio/webhook/', TwilioWebhookView.as_view(), name='twilio-webhook'),
    path('api/notifications/', include('notifications.urls')),
    
    # Auth
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/jwt/', include('accounts.jwt_urls')),
    path('api/accounts/', include('accounts.urls')),
]