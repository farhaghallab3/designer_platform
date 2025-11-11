import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Payment
from orders.models import Order

class CreateTabbyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, client=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Example Tabby API request payload
        payload = {
            "payment": {
                "amount": order.price_cents / 100,
                "currency": "SAR",
                "description": order.project_name,
                "buyer": {
                    "email": order.email,
                    "phone": order.phone,
                    "name": request.user.username,
                },
                "merchant_urls": {
                    "success": "https://yourfrontend.com/payment-success",
                    "cancel": "https://yourfrontend.com/payment-cancel",
                    "failure": "https://yourfrontend.com/payment-failed",
                }
            }
        }

        headers = {
            "Authorization": "Bearer YOUR_TABBY_SECRET_KEY",
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.tabby.ai/api/v2/checkout", json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            payment_url = data["configuration"]["available_products"]["installments"][0]["web_url"]

            Payment.objects.create(
                order=order,
                provider="tabby",
                payment_url=payment_url
            )

            return Response({"payment_url": payment_url})
        else:
            return Response({"error": response.text}, status=response.status_code)
class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        event = request.data
        transaction_id = event.get("id")
        status_update = event.get("status")

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.status = status_update
            payment.save()
        except Payment.DoesNotExist:
            pass

        return Response({"status": "ok"})
