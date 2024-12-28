from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema_view

from reservations import swagger
from reservations.models import Reserve, CancelledReserve
from reservations.serializers import ReserveSerializer, CancelledReserveSerializer
from reservations.permissions import IsReserveOwner, IsCancelledReserveOwner
from rooms.permissions import ReadOnly
from payments.models import Bill
from payments.serializers import BillSerializer
from payments.permissions import IsBillOwner


@extend_schema_view(**swagger.reserve_list_view)
class ReserveListView(generics.ListAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser]
    

@extend_schema_view(**swagger.reserve_detail_view)
class ReserveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser|(ReadOnly&IsReserveOwner)]
    

@extend_schema_view(**swagger.cancel_reserve_view)
class CancelReserveView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser|IsCancelledReserveOwner]
    queryset = CancelledReserve.objects.all()
    serializer_class = CancelledReserveSerializer
    lookup_field = 'reserve__id'
    
    def post(self, request, reserve__id):
        reserve = get_object_or_404(Reserve, id=reserve__id)
        if not (IsAdminUser|IsReserveOwner)().has_object_permission(request, self, reserve):
            raise PermissionDenied()
        cancel = CancelledReserve.objects.create(reserve=reserve, penalty=reserve.price//2)
        reserve.status = Reserve.CANCELED
        reserve.save()
        return Response(CancelledReserveSerializer(cancel).data, status=status.HTTP_201_CREATED)
    

@extend_schema_view(**swagger.reserve_bill_view)   
class ReserveBillView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser|IsBillOwner]
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    lookup_field = 'reserve__id'
