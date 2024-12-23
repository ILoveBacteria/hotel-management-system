from django.db.models import Q

from reservations.models import Reserve
  

def get_candidate_rooms(room_type):
    return room_type.rooms.filter(is_active=True)


def is_reserve_overlapped(room, check_in, check_out):
    return room.reserves.filter(
        ~(Q(check_out__lte=check_in) | Q(check_in__gte=check_out)),
        ~Q(status=Reserve.CANCELED),
    ).exists()
