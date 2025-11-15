from rest_framework import serializers
from .models import User, Message, Conversation



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer(read_only = True)
    sender_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at']
    
    def get_sender_full_name(self, obj):
        return f"{obj.sender_id.first_name} {obj.sender_id.last_name}"
    
    def validate_message_body(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Message body should not be less than 10 characters')
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants_id = UserSerializer(read_only = True)

    # Example CharField for temporary notes
    conversation_note = serializers.CharField(max_length=255, required=False, allow_blank=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']