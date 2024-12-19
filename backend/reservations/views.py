from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from reservations.models import Reserve
from reservations.serializers import ReserveSerializer
from reservations.permissions import IsOwner


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