# payment/models.py
from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50)  # 'tabby' or 'tamara'
    payment_url = models.URLField()
    status = models.CharField(max_length=20, default='pending')  # pending, paid, failed
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
