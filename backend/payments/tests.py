from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse

from payments.models import Bill
from reservations.models import Reserve

from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from reservations.signals import update_bill_status
from django.db.models.signals import post_save
from rest_framework import status

from rooms.models import RoomType


def disable_post_save(signal, sender, receiver):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.disconnect(receiver, sender=sender)
            try:
                return func(*args, **kwargs)
            finally:
                # Reconnect the signal
                signal.connect(receiver, sender=sender)
        return wrapper
    return decorator


class PayBillTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name='Test Room Type', price=100, double_beds=1, single_beds=1, description='Test Description')
        self.room0 = self.room_type.rooms.create(room_number=100, is_active=True) 
        self.room1 = self.room_type.rooms.create(room_number=101, is_active=True)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
    
    @disable_post_save(post_save, Reserve, update_bill_status)
    def test_overdue_bill(self):
        reserve = Reserve.objects.create(room=self.room0, check_in='2025-02-02', check_out='2025-02-05', status=Reserve.REGISTERED, price=100, user=self.user)
        bill = Bill.objects.create(reserve=reserve, amount=100, due_date='2025-02-06')
        bill.status = Bill.OVERDUE
        bill.save()
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('pay-bill', kwargs={'pk': bill.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    @disable_post_save(post_save, Reserve, update_bill_status)
    def test_paid_bill(self):
        reserve = Reserve.objects.create(room=self.room0, check_in='2025-02-02', check_out='2025-02-05', status=Reserve.REGISTERED, price=100, user=self.user)
        bill = Bill.objects.create(reserve=reserve, amount=100, due_date='2025-02-06', status=Bill.PAID, payment_date=timezone.now())
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('pay-bill', kwargs={'pk': bill.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    @disable_post_save(post_save, Reserve, update_bill_status)
    def test_only_bill_owner_can_pay(self):
        reserve = Reserve.objects.create(room=self.room0, check_in='2025-02-02', check_out='2025-02-05', status=Reserve.REGISTERED, price=100, user=self.user)
        bill = Bill.objects.create(reserve=reserve, amount=100, due_date='2025-02-06')
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('pay-bill', kwargs={'pk': bill.id}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        client.logout()
        client.login(username='testuser2', password='testpassword')
        response = client.get(reverse('pay-bill', kwargs={'pk': bill.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)