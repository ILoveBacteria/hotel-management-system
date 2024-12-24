from rest_framework import generics
from drf_spectacular.utils import extend_schema_view
from rest_framework.permissions import IsAdminUser

from payments import swagger
from payments.models import Bill
from payments.serializers import BillSerializer
from payments.permissions import IsBillOwner


@extend_schema_view(**swagger.bill_list_view)
class BillListView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAdminUser]
    

@extend_schema_view(**swagger.bill_detail_view)
class BillDetailView(generics.RetrieveAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAdminUser|IsBillOwner]
