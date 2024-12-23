from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema_view

from rooms import swagger
from rooms.models import Room, RoomType, RoomImage
from rooms.serializers import RoomSerializer, RoomTypeSerializer, RoomImageSerializer
from rooms.permissions import ReadOnly
from reservations.models import Reserve
from reservations.serializers import ReserveCreateSerializer


@extend_schema_view(**swagger.room_viewset)
class RoomViewSet(mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
    

@extend_schema_view(**swagger.room_type_viewset)
class RoomTypeViewSet(viewsets.ModelViewSet):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
    
    
@extend_schema_view(**swagger.room_image_viewset)
class RoomImageViewSet(mixins.ListModelMixin, 
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = RoomImageSerializer
    queryset = RoomImage.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
    

class BaseRoomTypeRelation(mixins.ListModelMixin, 
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin, 
                           viewsets.GenericViewSet):
    permission_classes = [IsAdminUser|ReadOnly]
    relation_class = None
    
    def get_queryset(self):
        room_type = get_object_or_404(RoomType, id=self.kwargs['room_type'])
        return self.relation_class.objects.filter(room_type=room_type)
    
    def perform_create(self, serializer):
        room_type = get_object_or_404(RoomType, id=self.kwargs['room_type'])
        serializer.validated_data['room_type'] = room_type
        return super().perform_create(serializer)
    

@extend_schema_view(**swagger.room_type_image_viewset)
class RoomTypeImageViewSet(BaseRoomTypeRelation):
    serializer_class = RoomImageSerializer
    relation_class = RoomImage
    

@extend_schema_view(**swagger.room_type_inventory_viewset)
class RoomTypeInventoryViewSet(BaseRoomTypeRelation):
    serializer_class = RoomSerializer
    relation_class = Room


@extend_schema_view(**swagger.current_user_reserve_view)
class CurrentUserReserveView(generics.CreateAPIView):
    serializer_class = ReserveCreateSerializer
    permission_classes = [IsAuthenticated]
