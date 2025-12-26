from django.urls import path, include
from rest_framework import routers
from .views import MessageViewSet, ConversationViewSet


router = routers.DefaultRouter()
router.register(r'conversation', ConversationViewSet)

# conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
# conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<uuid:conversation_id>/messages/', 
         MessageViewSet.as_view({ 
        'post': 'create',
        'get': 'list'
    })),
    path('conversations/<uuid:conversation_id>/messages/<int:pk>/', 
        MessageViewSet.as_view({      
            'put': 'update',        
            'patch': 'partial_update',  
            'delete': 'destroy'
        }), 
        name='conversation-message-detail'
    ),
]