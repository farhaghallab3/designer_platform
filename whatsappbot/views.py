import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order  # ✅ Access your orders
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

# 🌐 Green API constants
GREEN_API_URL = "https://api.green-api.com"
ID_INSTANCE = "7107377441"  # Your instance ID
API_TOKEN = "accf25cca26d4769a87a317285c656d7af84fca6eb8c41a084"  # Your API token


def send_message(chat_id, text):
    """Send a message via Green API"""
    url = f"{GREEN_API_URL}/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": chat_id, "message": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Error sending message:", e)


@csrf_exempt
def whatsapp_webhook(request):
    """Receive messages from WhatsApp (automatic order tracking)"""
    if request.method == "GET":
        return JsonResponse({"status": "ready"}, status=200)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("messageData", {}).get("textMessageData", {}).get("textMessage", "").strip()
            chat_id = data.get("senderData", {}).get("chatId")

            if not chat_id:
                return JsonResponse({"error": "No chat ID"}, status=400)

            # ✅ When user chooses 1 — automatically get their orders
            if message == "1":
                phone_number = chat_id.replace("@c.us", "")
                orders = Order.objects.filter(phone_number=phone_number)
                if orders.exists():
                    reply = "📦 Your orders:\n"
                    for order in orders:
                        reply += f"• #{order.id} - {order.status}\n"
                    send_message(chat_id, reply)
                else:
                    send_message(chat_id, "❌ No orders found for your account.")

            elif message == "2":
                send_message(chat_id, "👩‍🎨 Connecting you with your designer...")

            elif message == "3":
                send_message(chat_id, "💼 Connecting you with our marketing team...")

            else:
                send_message(
                    chat_id,
                    "👋 Hello! Choose one: 1️⃣ Track order status 2️⃣ Contact my designer 3️⃣ Contact the marketer"
                )

            return JsonResponse({"status": "ok"}, status=200)

        except Exception as e:
            print("Webhook error:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"detail": "Invalid request method"}, status=405)


# ✅ API version (used by frontend)
class ChatBotAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")
        phone_number = request.data.get("phone")

        if not user_message:
            return Response({"error": "Message is required"}, status=400)

        id_instance = settings.GREEN_API_ID_INSTANCE
        api_token = settings.GREEN_API_TOKEN

        # ✅ If user selects "1", automatically get orders by phone_number
        if user_message == "1" and phone_number:
            orders = Order.objects.filter(phone_number=phone_number)
            if orders.exists():
                reply_text = "📦 Your orders:\n"
                for order in orders:
                    reply_text += f"• #{order.id} - {order.status}\n"
            else:
                reply_text = "❌ No orders found for your account."

        elif user_message == "2":
            reply_text = "👩‍🎨 Connecting you with your designer..."
        elif user_message == "3":
            reply_text = "💼 Connecting you with our marketing team..."
        else:
            reply_text = "👋 Hello! Choose: 1️⃣ Track order 2️⃣ Contact designer 3️⃣ Contact marketer"

        # Send WhatsApp message automatically
        if phone_number:
            send_url = f"{GREEN_API_URL}/waInstance{id_instance}/SendMessage/{api_token}"
            payload = {
                "chatId": f"{phone_number}@c.us",
                "message": reply_text
            }
            try:
                requests.post(send_url, json=payload)
            except Exception as e:
                print("Error sending message:", e)

        return Response({"reply": reply_text})
