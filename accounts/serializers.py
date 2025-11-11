# accounts/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_designer', 'phone_number', 'profile_image', 'bio')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_designer=validated_data.get('is_designer', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
