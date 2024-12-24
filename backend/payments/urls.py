from django.urls import path

from payments.views import BillListView, BillDetailView


urlpatterns = [
    path('bills/', BillListView.as_view(), name='bill-list'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
]
