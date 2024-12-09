from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema_view

from users.serializers import UserProfileSerializer
from users.permissions import IsOwner
from users.swagger import current_user_profile, user_profile

from reservations.models import Reserve
from reservations.serializers import ReserveSerializer


@extend_schema_view(**user_profile)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAdminUser|IsOwner]
    

@extend_schema_view(**current_user_profile)
class CurrentUserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CurrentUserReservesView(generics.ListCreateAPIView):
    serializer_class = ReserveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reserve.objects.filter(user=self.request.user)
    
    
class UserReservesView(generics.ListAPIView):
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Reserve.objects.filter(user_id=self.kwargs['pk'])
