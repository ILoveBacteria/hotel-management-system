from rest_framework import generics
from rest_framework import permissions
from drf_spectacular.utils import extend_schema_view

from messages_.models import Message
from messages_.serializers import MessageSerializer
from messages_ import swagger

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
