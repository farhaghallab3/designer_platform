# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.twiml.messaging_response import MessagingResponse
from orders.models import Order


class TwilioWebhookView(APIView):
    authentication_classes = []  # Twilio doesn't send auth
    permission_classes = []

    def post(self, request, *args, **kwargs):
        incoming_msg = request.data.get('Body', '').strip().lower()
        from_number = request.data.get('From', '')
        response = MessagingResponse()
        msg = response.message()

        # Normalize phone number for DB lookup
        phone = from_number.replace('whatsapp:', '').replace('+', '')

        # 🔹 Logic handling user messages
        if "track" in incoming_msg:
            order = Order.objects.filter(phone__icontains=phone).last()
            if order:
                msg.body(f"📦 Your order *{order.project_name}* is currently *{order.status}*.")
            else:
                msg.body("❌ Sorry, no orders found under your number.")
        elif "designer" in incoming_msg:
            msg.body("🎨 Your designer will contact you soon.")
        elif "marketer" in incoming_msg:
            msg.body("💬 Our marketing team will reach out shortly.")
        else:
            msg.body(
                "👋 Welcome to DesignHub!\n\n"
                "Please reply with one of the following:\n"
                "1️⃣ Track order status\n"
                "2️⃣ Contact my designer\n"
                "3️⃣ Contact the marketer"
            )

        return Response(str(response), status=status.HTTP_200_OK, content_type="application/xml")
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

def whatsapp_webhook(request):
    from_number = request.POST.get('From')
    incoming_msg = request.POST.get('Body', '').strip().lower()

    resp = MessagingResponse()
    msg = resp.message()

    if 'track' in incoming_msg:
        msg.body("📦 Your order is being processed and will be delivered soon.")
    elif 'designer' in incoming_msg:
        msg.body("🎨 Your designer will contact you shortly!")
    elif 'marketer' in incoming_msg:
        msg.body("📣 Our marketing team will reach out soon!")
    else:
        msg.body("👋 Welcome! Reply with one of the following:\n• Track order status\n• Contact my designer\n• Contact the marketer")

    return HttpResponse(str(resp), content_type='text/xml')
