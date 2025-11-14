from django.contrib import admin
from .models import Order, OrderFile

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'client', 'designer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['project_name', 'client__username', 'designer__user__username']

@admin.register(OrderFile)
class OrderFileAdmin(admin.ModelAdmin):
    list_display = ['order', 'file', 'uploaded_at']
    list_filter = ['uploaded_at']