from rest_framework import serializers
from .models import Order, OrderFile

class OrderFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFile
        fields = ['id','file','uploaded_at']

class OrderSerializer(serializers.ModelSerializer):
    files = OrderFileSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','client','designer','package','project_name','product_description','email','phone','price_cents','status','payment_verified','created_at','files']
        read_only_fields = ['client','status','payment_verified','created_at']
