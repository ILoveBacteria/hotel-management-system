from django.urls import path
from rest_framework.routers import DefaultRouter

from rooms.views import RoomViewSet


router = DefaultRouter()
router.register(r'', RoomViewSet, basename='user')

urlpatterns = [
]

urlpatterns += router.urls
