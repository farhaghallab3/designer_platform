from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

@shared_task
def send_order_received_messages(order_id):
    from orders.models import Order
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    # send email (lightweight)
    try:
        send_mail(
            subject=f'Order {order.id} received',
            message=f'Hello {order.client.get_full_name() or order.client.username},\n\nWe received your order #{order.id}. We will review and contact you soon.',
            from_email='no-reply@example.com',
            recipient_list=[order.email],
            fail_silently=True
        )
    except Exception:
        pass

    # send whatsapp/sms via Twilio
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        to_whatsapp = f'whatsapp:{order.phone}'
        client.messages.create(
            body=f"Your order {order.id} has been received and is under review. Visit {settings.FRONTEND_URL}/dashboard to track it.",
            from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
            to=to_whatsapp
        )
    except Exception:
        pass

    # notify designer
    try:
        if order.designer and order.designer.user.phone_number:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            to_whatsapp = f'whatsapp:{order.designer.user.phone_number}'
            client.messages.create(
                body=f"New order assigned: {order.project_name}. Client: {order.client.get_full_name() or order.client.username}, phone: {order.phone}.",
                from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
                to=to_whatsapp
            )
    except Exception:
        pass
