from django.urls import path

from reservations.views import ReserveListView, ReserveDetailView, CancelReserveView, ReserveBillView


urlpatterns = [
    path('reserves/', ReserveListView.as_view(), name='reserves-list'),
    path('reserves/<int:pk>/', ReserveDetailView.as_view(), name='reserves-detail'),
    path('reserves/<int:reserve__id>/cancel/', CancelReserveView.as_view(), name='reserves-cancel'),
    path('reserves/<int:reserve__id>/bill/', ReserveBillView.as_view(), name='reserves-bill'),
]
