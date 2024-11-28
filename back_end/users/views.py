from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView

from users.models import GuestProfile
from users.serializers import UserProfileSerializer


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()
    

class CurrentUserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
