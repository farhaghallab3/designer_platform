from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(
        'orders.Order', 
        on_delete=models.CASCADE,
        default=None, 
        null=True
    )
    provider = models.CharField(max_length=50, default='tabby')
    payment_url = models.URLField()
    status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)