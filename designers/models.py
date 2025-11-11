from django.db import models
from django.conf import settings

class Package(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price_cents = models.IntegerField()
    duration_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price_cents/100:.2f}"

class DesignerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='designer_profile')
    portfolio = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
