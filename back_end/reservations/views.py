from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from reservations.models import Reserve
from reservations.serializers import ReserveSerializer


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class ReserveListView(generics.ListAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser]
    

class ReserveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser]