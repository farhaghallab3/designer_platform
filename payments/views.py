# payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(APIView):
    def post(self, request):
        try:
            order_id = request.data.get("order_id")
            order = Order.objects.get(id=order_id)
            amount = int(order.package.price * 100)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": amount,
                            "product_data": {"name": order.package.name},
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=settings.FRONTEND_URL + "/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.FRONTEND_URL + "/cancel",
                metadata={"order_id": order.id},
            )
            return Response({"sessionId": checkout_session["id"]})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhook(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session["metadata"]["order_id"]
            order = Order.objects.get(id=order_id)
            order.status = "Paid"
            order.save()

        return HttpResponse(status=200)
