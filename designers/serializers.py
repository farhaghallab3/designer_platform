from rest_framework import serializers
from .models import Package, DesignerProfile
from accounts.serializers import UserSerializer

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class DesignerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # ✅ <-- just add read_only=True

    class Meta:
        model = DesignerProfile
        fields = ['id', 'user', 'portfolio', 'rating']
