from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from reservations.models import Reserve
from reservations.serializers import ReserveSerializer
from payments.models import Bill
from payments.serializers import BillSerializer


class IsReserveOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class IsBillOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.reserve.user == request.user


class ReserveListView(generics.ListAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser]
    

class ReserveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser|IsReserveOwner]
    
    
class CancelReserveView(views.APIView):
    permission_classes = [IsAdminUser|IsReserveOwner]
    
    def post(self, request, pk):
        # TODO: Implement the logic to cancel a reservation
        return Response('No Logic', status=500)
    

class ReserveBillView(generics.RetrieveAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAdminUser|IsBillOwner]
    lookup_field = 'reserve_id'
    