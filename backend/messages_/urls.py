from django.urls import path

from messages_.views import MessageCreateView, MessageListView, MessageDetailView


urlpatterns = [
    path('', MessageListView.as_view(), name='list-messages'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('create/', MessageCreateView.as_view(), name='create-message'),
]
