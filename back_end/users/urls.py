from django.urls import path
from users.views import UserProfileView, CurrentUserProfileView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
]
