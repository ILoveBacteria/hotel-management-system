from django.urls import path
from rest_framework.routers import SimpleRouter

from rooms.views import RoomViewSet, RoomTypeViewSet, RoomImageViewSet, RoomTypeImageViewSet, RoomTypeInventoryViewSet, CurrentUserReserveView


router = SimpleRouter(use_regex_path=False)
router.register('inventories', RoomViewSet)
router.register('types', RoomTypeViewSet)
router.register('images', RoomImageViewSet, basename='images')
# Query routers
router.register('types/<int:room_type>/images', RoomTypeImageViewSet, basename='room-type-images')
router.register('types/<int:room_type>/inventories', RoomTypeInventoryViewSet, basename='room-type-inventories')

urlpatterns = [
    path('types/<int:room_type>/reserve/', CurrentUserReserveView.as_view(), name='current-user-reserve'),
]

urlpatterns += router.urls
