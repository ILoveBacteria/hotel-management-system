from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from reservations.models import Reserve
from rooms.models import RoomType


class ReserveSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name='user-profile', read_only=True)
    room = serializers.HyperlinkedIdentityField(view_name='inventories-detail', read_only=True)
    
    class Meta:
        model = Reserve
        fields = '__all__'
        read_only_fields = ['user', 'room', 'price', 'check_in', 'check_out']
        
    def validate(self, data):
        request = self.context.get('request')
        if 'status' in data and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to set the status field.")
        return data
        
        
class ReserveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['check_in', 'check_out']
        
    def validate(self, data):
        # TODO: Implement a better way to select a random room and check constraints.
        # TODO: Is this room available on that date?
        view = self.context.get('view')
        room_type = get_object_or_404(RoomType, id=view.kwargs['room_type'])
        if room_type.rooms.count() == 0:
            raise serializers.ValidationError('There are no rooms available for this room type.')
        data['room_type'] = room_type
        return data
        
    def create(self, validated_data):
        request = self.context.get('request')
        room_type = validated_data.pop('room_type')
        random_room = self.pick_random_available_room(room_type)
        validated_data['room'] = random_room
        validated_data['user'] = request.user
        validated_data['price'] = room_type.price
        return super().create(validated_data)
    
    def pick_random_available_room(self, room_type):
        return room_type.rooms.first()
