from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema_view

from users.serializers import UserProfileSerializer
from users.permissions import IsOwner
from users import swagger

from reservations.models import Reserve
from reservations.serializers import ReserveSerializer


@extend_schema_view(**swagger.user_profile)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAdminUser|IsOwner]
    

@extend_schema_view(**swagger.current_user_profile)
class CurrentUserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(**swagger.current_user_reserves_view)
class CurrentUserReservesView(generics.ListAPIView):
    serializer_class = ReserveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reserve.objects.filter(user=self.request.user)
    

@extend_schema_view(**swagger.user_reserves_view)
class UserReservesView(generics.ListAPIView):
    serializer_class = ReserveSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs['user_id'])
        return Reserve.objects.filter(user=user)
