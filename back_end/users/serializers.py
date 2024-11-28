from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import GuestProfile


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        exclude = ['id', 'user']


class UserProfileSerializer(serializers.ModelSerializer):
    guest_profile = GuestProfileSerializer()
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'is_staff', 'is_active', 'is_superuser', 'guest_profile')
        read_only_fields = ['email', 'username', 'is_staff', 'is_active', 'is_superuser']
