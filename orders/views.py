from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from .models import Order, OrderFile
from .serializers import OrderSerializer, OrderFileSerializer

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
        order = serializer.save(client=self.request.user)
        # Send notification if Twilio is configured
        self.send_order_notification(order)

    def create(self, request, *args, **kwargs):
        # Handle file uploads in the create method
        files = request.FILES.getlist('files')
        
        # Create the order first
        response = super().create(request, *args, **kwargs)
        
        # If order was created successfully, handle file uploads
        if response.status_code == status.HTTP_201_CREATED and files:
            order_id = response.data['id']
            order = Order.objects.get(id=order_id)
            
            uploaded_files = []
            for file in files:
                order_file = OrderFile.objects.create(order=order, file=file)
                uploaded_files.append({
                    'name': file.name,
                    'url': order_file.file.url
                })
            
            # Update the order with file information
            order.files = uploaded_files
            order.save()
            
            # Update response data to include files
            response.data['files'] = uploaded_files

        return response

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_file(self, request, pk=None):
        order = self.get_object()
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({'detail': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        order_file = OrderFile.objects.create(order=order, file=file_obj)
        
        # Update the order's files JSON field
        if not order.files:
            order.files = []
        
        order.files.append({
            'name': file_obj.name,
            'url': order_file.file.url,
            'uploaded_at': order_file.uploaded_at.isoformat()
        })
        order.save()
        
        return Response(OrderFileSerializer(order_file).data, status=status.HTTP_201_CREATED)

    def send_order_notification(self, order):
        """Send WhatsApp/SMS notification when order is created"""
        try:
            # Only send if Twilio is configured
            if (hasattr(settings, 'TWILIO_ACCOUNT_SID') and 
                hasattr(settings, 'TWILIO_AUTH_TOKEN') and 
                hasattr(settings, 'TWILIO_WHATSAPP_NUMBER')):
                
                from twilio.rest import Client
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

                message_text = f"مرحباً {order.full_name}، تم استلام طلبك '{order.project_name}' بنجاح وجاري المراجعة. سنتواصل معك قريباً."

                # WhatsApp message
                client.messages.create(
                    from_=settings.TWILIO_WHATSAPP_NUMBER,
                    to=f"whatsapp:{order.phone}",
                    body=message_text
                )

                # Optional: SMS fallback
                if hasattr(settings, 'TWILIO_SMS_NUMBER'):
                    client.messages.create(
                        from_=settings.TWILIO_SMS_NUMBER,
                        to=order.phone,
                        body=message_text
                    )
                    
        except Exception as e:
            # Log the error but don't break the order creation
            print(f"Failed to send notification: {e}")

def send_order_whatsapp(to_number, order_id):
    """Utility function to send WhatsApp message"""
    try:
        if (hasattr(settings, 'TWILIO_ACCOUNT_SID') and 
            hasattr(settings, 'TWILIO_AUTH_TOKEN') and 
            hasattr(settings, 'TWILIO_WHATSAPP_NUMBER')):
            
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = f"✅ تم استلام طلبك #{order_id} بنجاح وجاري المراجعة. سنتواصل معك قريباً!"
            client.messages.create(
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=f"whatsapp:{to_number}",
                body=message
            )
    except Exception as e:
        print(f"Failed to send WhatsApp: {e}")