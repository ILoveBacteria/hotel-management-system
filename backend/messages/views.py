from rest_framework import generics
from rest_framework import permissions
from drf_spectacular.utils import extend_schema_view

from messages.models import Message
from messages.serializers import MessageSerializer
from messages import swagger

@extend_schema_view(**swagger.message_create_view)
class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    

@extend_schema_view(**swagger.message_list_view)
class MessageListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]
    

@extend_schema_view(**swagger.message_detail_view)
class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]
