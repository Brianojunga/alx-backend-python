from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsConversationParticipant, IsMessageSender
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant, IsMessageSender]

    # Example: override create to automatically set sender
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]

    # Optional: add filtering by participants
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants_id__first_name', 'participants_id__last_name']
