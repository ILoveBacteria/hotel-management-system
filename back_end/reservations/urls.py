from django.urls import path

from reservations.views import ReserveListView, ReserveDetailView


urlpatterns = [
    path('reserves/', ReserveListView.as_view(), name='reserves-list'),
    path('reserves/<int:pk>/', ReserveDetailView.as_view(), name='reserves-detail'),
]
