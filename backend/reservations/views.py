from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema_view

from reservations import swagger
from reservations.models import Reserve
from reservations.serializers import ReserveSerializer
from reservations.permissions import IsOwner
from rooms.permissions import ReadOnly


@extend_schema_view(**swagger.reserve_list_view)
class ReserveListView(generics.ListAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser]
    

@extend_schema_view(**swagger.reserve_detail_view)
class ReserveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser|(ReadOnly&IsOwner)]
    

@extend_schema_view(**swagger.cancel_reserve_view)
class CancelReserveView(views.APIView):
    permission_classes = [IsAdminUser|IsOwner]
    
    def post(self, request, pk):
        # TODO: Implement the logic to cancel a reservation
        return Response('No Logic', status=500)