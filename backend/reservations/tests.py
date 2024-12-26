from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User

from reservations.models import Reserve
from reservations import queries
from rooms.models import RoomType
from payments.models import Bill


class AvailableRoomsQueryTestCase(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(name='Test Room Type', price=100, double_beds=1, single_beds=1, description='Test Description')
        self.room0 = self.room_type.rooms.create(room_number=100, is_active=True) 
        self.room1 = self.room_type.rooms.create(room_number=101, is_active=True)
        self.room2 = self.room_type.rooms.create(room_number=102, is_active=True)
        self.room3 = self.room_type.rooms.create(room_number=103, is_active=True)
        self.room4 = self.room_type.rooms.create(room_number=104, is_active=True)
        self.room5 = self.room_type.rooms.create(room_number=105, is_active=True)
        self.room6 = self.room_type.rooms.create(room_number=106, is_active=False)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_overlap(self):
        Reserve.objects.create(room=self.room0, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room0, check_in='2021-01-03', check_out='2021-01-05', status=Reserve.REGISTERED, price=100, user=self.user)
        self.assertTrue(queries.is_reserve_overlapped(self.room0, '2021-01-01', '2021-01-02'))
        self.assertTrue(queries.is_reserve_overlapped(self.room0, '2021-01-01', '2021-01-03'))
        self.assertTrue(queries.is_reserve_overlapped(self.room0, '2021-01-01', '2021-01-04'))
        self.assertTrue(queries.is_reserve_overlapped(self.room0, '2021-01-01', '2021-01-05'))
        self.assertTrue(queries.is_reserve_overlapped(self.room0, '2021-01-04', '2021-01-05'))
        self.assertTrue(queries.is_reserve_overlapped(self.room0, '2021-01-04', '2021-01-08'))
        self.assertFalse(queries.is_reserve_overlapped(self.room0, '2021-01-02', '2021-01-03'))
        self.assertFalse(queries.is_reserve_overlapped(self.room0, '2021-01-05', '2021-01-07'))
        
        Reserve.objects.create(room=self.room1, check_in='2021-01-01', check_out='2021-01-03', status=Reserve.CANCELED, price=100, user=self.user)
        Reserve.objects.create(room=self.room1, check_in='2021-01-04', check_out='2021-01-07', status=Reserve.PAID, price=100, user=self.user)
        self.assertFalse(queries.is_reserve_overlapped(self.room1, '2021-01-01', '2021-01-03'))
        self.assertFalse(queries.is_reserve_overlapped(self.room1, '2021-01-01', '2021-01-04'))
        self.assertFalse(queries.is_reserve_overlapped(self.room1, '2021-01-02', '2021-01-04'))
        self.assertTrue(queries.is_reserve_overlapped(self.room1, '2021-01-02', '2021-01-05'))
        
    def test_candidate(self):
        self.assertEqual(queries.get_candidate_rooms(self.room_type).count(), 6)
        self.room6.is_active = True
        self.room6.save()
        self.assertEqual(queries.get_candidate_rooms(self.room_type).count(), 7)
        
    def test_reservable(self):
        Reserve.objects.create(room=self.room0, check_in='2021-01-01', check_out='2021-01-04', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room0, check_in='2021-01-07', check_out='2021-01-08', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room1, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room1, check_in='2021-01-05', check_out='2021-01-06', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room1, check_in='2021-01-07', check_out='2021-01-10', status=Reserve.REGISTERED, price=100, user=self.user)
        for room in queries.get_candidate_rooms(self.room_type):
            if room.room_number == 100 or room.room_number == 101:
                self.assertTrue(queries.is_reserve_overlapped(room, '2021-01-01', '2021-01-02'))
            else:
                self.assertFalse(queries.is_reserve_overlapped(room, '2021-01-01', '2021-01-02'))
                
        for room in queries.get_candidate_rooms(self.room_type):
            if room.room_number == 100 or room.room_number == 101:
                self.assertTrue(queries.is_reserve_overlapped(room, '2021-01-07', '2021-01-08'))
            else:
                self.assertFalse(queries.is_reserve_overlapped(room, '2021-01-07', '2021-01-08'))


class ReserveTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.room_type = RoomType.objects.create(name='Test Room Type', price=100, double_beds=1, single_beds=1, description='Test Description')
        self.room0 = self.room_type.rooms.create(room_number=100, is_active=True) 
        self.room1 = self.room_type.rooms.create(room_number=101, is_active=True)
        self.room2 = self.room_type.rooms.create(room_number=102, is_active=True)
        self.room3 = self.room_type.rooms.create(room_number=103, is_active=True)
        self.room4 = self.room_type.rooms.create(room_number=104, is_active=True)
        self.room5 = self.room_type.rooms.create(room_number=105, is_active=True)
        self.room6 = self.room_type.rooms.create(room_number=106, is_active=False)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
    def test_reserve_create(self):
        response = self.client.post(f'/rooms/types/{self.room_type.id}/reserve/', {'check_in': '2021-01-01', 'check_out': '2021-01-02'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Reserve.objects.count(), 1)
        reserve = Reserve.objects.first()
        self.assertEqual(reserve.room, self.room0)
        self.assertEqual(reserve.check_in, timezone.datetime(2021, 1, 1).date())
        self.assertEqual(reserve.check_out, timezone.datetime(2021, 1, 2).date())
        self.assertEqual(reserve.price, 100)
        self.assertEqual(reserve.user, self.user)
    
    def test_reserve_create_overlap(self):
        room_type = RoomType.objects.create(name='Test Room Type', price=100, double_beds=2, single_beds=1, description='Test Description')
        room = room_type.rooms.create(room_number=110, is_active=True)
        reserve = Reserve.objects.create(room=room, check_in='2021-01-01', check_out='2021-01-05', status=Reserve.REGISTERED, price=100, user=self.user)
        response = self.client.post(f'/rooms/types/{room_type.id}/reserve/', {'check_in': '2021-01-01', 'check_out': '2021-02-02'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reserve.objects.count(), 1)
        reserve.status = Reserve.CANCELED
        reserve.save()
        response = self.client.post(f'/rooms/types/{room_type.id}/reserve/', {'check_in': '2021-01-01', 'check_out': '2021-02-02'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Reserve.objects.count(), 2)
        
    def test_reserve_create_no_room(self):
        room_type = RoomType.objects.create(name='Test Room Type', price=100, double_beds=2, single_beds=1, description='Test Description')
        response = self.client.post(f'/rooms/types/{room_type.id}/reserve/', {'check_in': '2021-01-01', 'check_out': '2021-02-02'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reserve.objects.count(), 0)
        
    def test_reserve_create_no_room_available(self):
        Reserve.objects.create(room=self.room0, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room1, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room2, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room3, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room4, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        Reserve.objects.create(room=self.room5, check_in='2021-01-01', check_out='2021-01-02', status=Reserve.REGISTERED, price=100, user=self.user)
        response = self.client.post(f'/rooms/types/{self.room_type.id}/reserve/', {'check_in': '2021-01-01', 'check_out': '2021-02-02'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reserve.objects.count(), 6)
        
    def test_bill_generate(self):
        response = self.client.post(f'/rooms/types/{self.room_type.id}/reserve/', {'check_in': '2021-01-01', 'check_out': '2021-01-02'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bill.objects.count(), 1)
        bill = Bill.objects.first()
        self.assertEqual(bill.reserve, Reserve.objects.first())
        self.assertEqual(bill.amount, 100)
        
    def test_reserve_non_exist_room(self):
        response = self.client.post(f'/rooms/types/100/reserve/', {'check_in': '2021-01-01', 'check_out': '2021-01-02'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Reserve.objects.count(), 0)
        
    def test_check_in_before_check_out(self):
        response = self.client.post(f'/rooms/types/{self.room_type.id}/reserve/', {'check_in': '2021-01-02', 'check_out': '2021-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reserve.objects.count(), 0)
