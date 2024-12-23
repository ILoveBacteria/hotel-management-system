from django.test import TestCase
from django.contrib.auth.models import User

from reservations.models import Reserve
from reservations import queries
from rooms.models import RoomType


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
