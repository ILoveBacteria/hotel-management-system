from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView

from users.models import GuestProfile
from users.serializers import UserProfileSerializer


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()
    

class CurrentUserProfileView(LoginRequiredMixin, RetrieveAPIView):
    serializer_class = UserProfileSerializer
    login_url = '/auth/login/'

    def get_object(self):
        return self.request.user
