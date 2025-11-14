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

        # MOCK PAYMENT - For testing without real API
        mock_payment_url = "https://checkout.tabby.ai/mock-payment-page"
        mock_transaction_id = f"tabby_mock_{order_id}_{order.price_cents}"

        # Create payment record
        payment = Payment.objects.create(
            order=order,
            provider="tabby",
            payment_url=mock_payment_url,
            transaction_id=mock_transaction_id,
            status="pending"
        )

        return Response({
            "payment_url": mock_payment_url,
            "transaction_id": mock_transaction_id,
            "status": "pending",
            "message": "Mock payment created successfully"
        })

class MockPaymentSuccessView(APIView):
    """Simulate successful payment for testing"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, transaction_id):
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.status = "paid"
            payment.save()
            
            # Update order status if needed
            payment.order.status = "paid"  # Add this field to Order model if needed
            payment.order.save()
            
            return Response({"status": "payment_success", "transaction_id": transaction_id})
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # For mock testing, you can manually call this or use the MockPaymentSuccessView
        event = request.data
        transaction_id = event.get("id") or event.get("transaction_id")
        status_update = event.get("status")

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.status = status_update
            payment.save()
            
            # Update order status based on payment status
            if status_update == "paid":
                payment.order.status = "paid"  # Add this to your Order model
                payment.order.save()
                
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "ok"})