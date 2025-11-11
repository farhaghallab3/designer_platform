from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderFile
from .serializers import OrderSerializer, OrderFileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from twilio.rest import Client
from django.conf import settings


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(client=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_file(self, request, pk=None):
        order = self.get_object()
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail':'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        of = OrderFile.objects.create(order=order, file=file_obj)
        return Response(OrderFileSerializer(of).data, status=status.HTTP_201_CREATED)
def perform_create(self, serializer):
    order = serializer.save(client=self.request.user)
    self.send_order_notification(order)

def send_order_notification(self, order):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message_text = f"Hi {order.client.username}, your order '{order.project_name}' has been received and is under review. We’ll contact you soon."

    # WhatsApp message
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{order.phone}",  # client's WhatsApp
        body=message_text
    )

    # Optional: SMS fallback
    client.messages.create(
        from_=settings.TWILIO_SMS_NUMBER,
        to=order.phone,
        body=message_text
    )
from twilio.rest import Client
from django.conf import settings

def send_order_whatsapp(to_number, order_id):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = f"✅ Your order #{order_id} has been received and is under review. We’ll contact you soon!"
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{to_number}",
        body=message
    )
