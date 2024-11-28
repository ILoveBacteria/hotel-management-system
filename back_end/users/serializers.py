from django.contrib.auth import get_user_model
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
        
    def update(self, instance, validated_data):
        guest_profile = validated_data.pop('guest_profile', {})
        for attr, value in guest_profile.items():
            setattr(instance.guest_profile, attr, value)
        instance.guest_profile.save()
        return super().update(instance, validated_data)
