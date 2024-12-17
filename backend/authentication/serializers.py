from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import GuestProfile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        GuestProfile.objects.create(user=user)
        return user
    

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
