from django.urls import path

from reservations.views import ReserveListView, ReserveDetailView, CancelReserveView


urlpatterns = [
    path('reserves/', ReserveListView.as_view(), name='reserves-list'),
    path('reserves/<int:pk>/', ReserveDetailView.as_view(), name='reserves-detail'),
    path('reserves/<int:pk>/cancel/', CancelReserveView.as_view(), name='reserves-cancel'),
]
