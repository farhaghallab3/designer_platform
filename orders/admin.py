from django.contrib import admin
from .models import Order, OrderFile

class OrderFileInline(admin.TabularInline):
    model = OrderFile
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','project_name','client','designer','status','payment_verified','created_at')
    inlines = [OrderFileInline]
