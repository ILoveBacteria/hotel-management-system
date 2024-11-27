from django.urls import path, include

from users.views import UserProfileView

urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='user-profile'),
]
