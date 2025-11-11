from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from twilio.twiml.messaging_response import MessagingResponse

class TwilioWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        body = request.POST.get('Body', '').strip()
        from_number = request.POST.get('From', '')
        resp = MessagingResponse()
        # very small menu: expect '1', '2', '3'
        if body == '1':
            resp.message(f"Track orders: {settings.FRONTEND_URL}/dashboard")
        elif body == '2':
            resp.message("To contact your designer, open your dashboard and click 'Contact Designer'.")
        elif body == '3':
            resp.message("To contact the marketer, email marketer@example.com")
        else:
            resp.message("Welcome! Reply with:\n1 - Track order status\n2 - Contact my designer\n3 - Contact the marketer")
        return Response(str(resp), content_type='application/xml')
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from twilio.twiml.messaging_response import MessagingResponse

class TwilioWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        body = request.POST.get('Body', '').strip()
        from_number = request.POST.get('From', '')
        resp = MessagingResponse()
        # very small menu: expect '1', '2', '3'
        if body == '1':
            resp.message(f"Track orders: {settings.FRONTEND_URL}/dashboard")
        elif body == '2':
            resp.message("To contact your designer, open your dashboard and click 'Contact Designer'.")
        elif body == '3':
            resp.message("To contact the marketer, email marketer@example.com")
        else:
            resp.message("Welcome! Reply with:\n1 - Track order status\n2 - Contact my designer\n3 - Contact the marketer")
        return Response(str(resp), content_type='application/xml')
