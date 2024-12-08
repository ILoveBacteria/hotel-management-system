from rest_framework import serializers
from rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ['created_at', 'updated_at']
