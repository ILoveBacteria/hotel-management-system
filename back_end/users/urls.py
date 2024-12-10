from django.urls import path
from users.views import UserProfileView, CurrentUserProfileView, CurrentUserReservesView, UserReservesView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('reserve/', CurrentUserReservesView.as_view(), name='current-user-reserves'),
    path('<int:pk>/reserves/', UserReservesView.as_view(), name='user-reserves'),
]
