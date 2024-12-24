from django.urls import path
from users.views import UserProfileView, CurrentUserProfileView, CurrentUserReservesView, UserReservesView, CurrentUserBillsView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('reserves/', CurrentUserReservesView.as_view(), name='current-user-reserves'),
    path('<int:user_id>/reserves/', UserReservesView.as_view(), name='user-reserves'),
    path('bills/', CurrentUserBillsView.as_view(), name='current-user-bills'),
]
