from rest_framework import generics, views
from rest_framework.response import Response
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
    permission_classes = [IsAdminUser|IsOwner]
    
    
class CancelReserveView(views.APIView):
    permission_classes = [IsAdminUser|IsOwner]
    
    def post(self, request, pk):
        # TODO: Implement the logic to cancel a reservation
        return Response('No Logic', status=500)