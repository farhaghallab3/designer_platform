from rest_framework import serializers
from .models import Order, OrderFile

class OrderFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFile
        fields = ['id', 'file', 'uploaded_at']

class OrderSerializer(serializers.ModelSerializer):
    order_files = OrderFileSerializer(many=True, read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True)
    designer_name = serializers.CharField(source='designer.user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'client', 'package', 'package_name', 'designer', 'designer_name',
            'full_name', 'phone', 'email', 'project_name', 'description',
            'status', 'files', 'order_files', 'created_at', 'updated_at'
        ]
        read_only_fields = ['client', 'created_at', 'updated_at']