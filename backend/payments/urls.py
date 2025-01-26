from django.urls import path

from payments.views import BillListView, BillDetailView, PayBillView


urlpatterns = [
    path('bills/', BillListView.as_view(), name='bill-list'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('bills/<int:pk>/pay/', PayBillView.as_view(), name='pay-bill'),
]
