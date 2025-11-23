from django.urls import path, include
from rest_framework import routers
# from rest_framework_nested import routers
from .views import MessageViewSet, ConversationViewSet


router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversation', ConversationViewSet)

# conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
# conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(conversation_router.urls))
]