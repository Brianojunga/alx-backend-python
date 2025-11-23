from rest_framework.permissions import BasePermission

class IsConversationParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.participants_id or request.user == obj.host_id
    
class IsMessageSender(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender_id