from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from reservations import queries
from reservations.models import Reserve, CancelledReserve
from rooms.models import RoomType


class CancelledReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelledReserve
        exclude = ['reserve']
        read_only_fields = ['penalty']


class ReserveSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-profile', read_only=True)
    room = serializers.HyperlinkedRelatedField(view_name='inventories-detail', read_only=True)
    
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
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError({'check_in': 'Check-in must be before check-out.'})
        view = self.context.get('view')
        room_type = get_object_or_404(RoomType, id=view.kwargs['room_type'])
        data['room'] = self.pick_random_available_room(room_type, data)
        data['room_type'] = room_type
        return data
        
    def create(self, validated_data):
        request = self.context.get('request')
        room_type = validated_data.pop('room_type')
        validated_data['user'] = request.user
        validated_data['price'] = room_type.price
        return super().create(validated_data)
    
    def pick_random_available_room(self, room_type, data):
        rooms = queries.get_candidate_rooms(room_type)
        for room in rooms:
            if not queries.is_reserve_overlapped(room, data['check_in'], data['check_out']):
                return room
        raise serializers.ValidationError('There are no rooms available for this room type.')
