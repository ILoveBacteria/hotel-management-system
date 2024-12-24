from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from payments.models import Bill
from payments.serializers import BillSerializer
from payments.permissions import IsBillOwner


class BillListView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAdminUser]
    

class BillDetailView(generics.RetrieveAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAdminUser|IsBillOwner]
