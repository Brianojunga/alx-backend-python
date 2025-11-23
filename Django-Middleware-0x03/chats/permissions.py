from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.participants_id or request.user == obj.host_id
    
class IsMessageSender(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender_id
    
class IsParticipantOfConversation(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # User must be authenticated to access the API
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        if request.method not in allowed_methods:
            return False
        
         # Conversation object (single participant or host/guest)
        if hasattr(obj, 'participants_id'):
            return obj.participants_id == request.user or obj.host_id == request.user

        # Message object
        elif hasattr(obj, 'conversation'):
            conversation = obj.conversation
            # Check if user is sender OR a participant OR host
            return (
                getattr(obj, 'sender_id', None) == request.user
                or getattr(conversation, 'participants_id', None) == request.user
                or getattr(conversation, 'host_id', None) == request.user
            )
        return False
            