from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from drf_spectacular.utils import extend_schema_view

from users.serializers import UserProfileSerializer
from users.permissions import IsOwner
from users.swagger import current_user_profile, user_profile


@extend_schema_view(**user_profile)
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAdminUser|IsOwner]
    

@extend_schema_view(**current_user_profile)
class CurrentUserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
