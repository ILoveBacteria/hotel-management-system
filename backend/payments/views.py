from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework.views import Response
from drf_spectacular.utils import extend_schema_view
from rest_framework.permissions import IsAdminUser

from payments import swagger
from payments.models import Bill
from payments.forms import CardForm
from payments.serializers import BillSerializer
from payments.permissions import IsBillOwner
from reservations.models import Reserve


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
    
    def get(self, request, *args, **kwargs):
        bill = self.get_object()
        if bill.status == Bill.PAID:
            return Response({'message': 'Bill already paid'}, status=status.HTTP_400_BAD_REQUEST)
        elif bill.status == Bill.OVERDUE or timezone.now() > bill.due_date:
            return Response({'message': 'Bill is overdue.'}, status=status.HTTP_400_BAD_REQUEST)
        return redirect(f'https://ipg.moeinarabi.ir/payments/pay/{bill.id}')
    

class PaymentGatewayView(View):
    def get(self, request, bill_id):
        bill = get_object_or_404(Bill, id=bill_id)
        if not bill.status == Bill.WAITING:
            return redirect('https://hotel.moeinarabi.ir/user/dashboard/payments')
        time_out_seconds = (bill.due_date - timezone.now()).total_seconds()
        hotel_name = 'هتل داری'
        context = {
            'bill': bill,
            'time_out': time_out_seconds,
            'hotel_name': hotel_name,
            'cancel_button': 'https://hotel.moeinarabi.ir/user/dashboard/payments',
        }
        return render(request, 'payments/payment_gateway.html', context)
    
    def post(self, request, bill_id):
        bill = get_object_or_404(Bill, id=bill_id)
        card_form = CardForm(request.POST)
        if not card_form.is_valid():
            return redirect(f'https://ipg.moeinarabi.ir/payments/pay/{bill.id}')
        card = card_form.save(commit=False)
        card.bill = bill
        card.save()
        bill.status = Bill.PAID
        bill.payment_date = timezone.now()
        bill.save()
        bill.reserve.status = Reserve.PAID
        bill.reserve.save()
        if bill.reserve.user.email:
            send_mail(
                subject='Payment Done',
                message=f'Payment for bill {bill.id} is done successfully.\nCheck-in date: {bill.reserve.check_in_date}\nCheck-out date: {bill.reserve.check_out_date}\nRoom: {bill.reserve.room.name}\nTotal price: {bill.total_price}',
                from_email='admin@moeinarabi.ir',
                recipient_list=[bill.reserve.user.email],
                fail_silently=False,
            )   
        return redirect('https://hotel.moeinarabi.ir/user/dashboard/payments')
