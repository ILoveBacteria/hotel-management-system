from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAdminUser

from rooms.models import Room, RoomType, RoomImage
from rooms.serializers import RoomSerializer, RoomTypeSerializer, RoomImageSerializer

from rooms.permissions import ReadOnly


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
    
    
class RoomTypeViewSet(viewsets.ModelViewSet):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
    
    
class RoomImageViewSet(viewsets.ModelViewSet):
    serializer_class = RoomImageSerializer
    queryset = RoomImage.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
    
    
class RoomTypeImageViewSet(mixins.ListModelMixin, 
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin, 
                           viewsets.GenericViewSet):
    serializer_class = RoomImageSerializer
    permission_classes = [IsAdminUser|ReadOnly]
    
    def get_queryset(self):
        return RoomImage.objects.filter(room_type_id=self.kwargs['room_type'])
