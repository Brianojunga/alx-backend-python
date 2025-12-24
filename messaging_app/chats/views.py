from django.shortcuts import render
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsConversationParticipant, IsMessageSender, IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant, IsMessageSender]
    pagination_class = MessagePagination

    # Example: override create to automatically set sender
    def create(self, request, *args, **kwargs):
        sender_id = request.user
        conversation_id = self.kwargs['conversation_id']
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            sender_id = sender_id,
            conversation = conversation,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def get_queryset(self):
        return Message.objects.filter(
                conversation = self.kwargs['conversation_id']
            )
    
    

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant, IsParticipantOfConversation]

    # Optional: add filtering by participants
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants_id__first_name', 'participants_id__last_name']
    filterset_class = MessageFilter

    def get_queryset(self):
        return Conversation.objects.filter(participants_id = self.request.user)
        
    def perfom_create(self, serializer):
        serializer.save(participants_id = self.request.user)