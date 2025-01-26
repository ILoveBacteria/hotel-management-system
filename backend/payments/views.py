from django.shortcuts import redirect
from django.utils import timezone

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
    

@extend_schema_view(**swagger.pay_bill_view) 
class PayBillView(generics.GenericAPIView):
    permission_classes = [IsBillOwner]
    queryset = Bill.objects.all()
    serializer_class = None
    
    def post(self, request, *args, **kwargs):
        bill = self.get_object()
        if bill.status == Bill.PAID:
            return Response({'message': 'Bill already paid'}, status=status.HTTP_400_BAD_REQUEST)
        elif bill.status == Bill.OVERDUE or timezone.now() > bill.due_date:
            return Response({'message': 'Bill is overdue.'}, status=status.HTTP_400_BAD_REQUEST)
        return redirect(f'https://ipg.moeinarabi.ir/payments/pay/{bill.id}')
