from rest_framework import serializers
from rooms.models import Room, RoomType, RoomImage


class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.HyperlinkedRelatedField(read_only=True, view_name='types-detail')

    class Meta:
        model = Room
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['room_type']
        

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        exclude = ['created_at', 'updated_at']
        

class RoomImageSerializer(serializers.ModelSerializer):
    room_type = serializers.HyperlinkedRelatedField(read_only=True, view_name='types-detail')
    
    class Meta:
        model = RoomImage
        exclude = ['updated_at']
        read_only_fields = ['room_type']
