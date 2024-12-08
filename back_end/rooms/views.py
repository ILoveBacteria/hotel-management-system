from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS

from rooms.models import Room
from rooms.serializers import RoomSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAdminUser|ReadOnly]
