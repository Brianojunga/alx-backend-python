from django.urls import path, include
from rest_framework import routers
from .views import MessageViewSet, ConversationViewSet


router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversation', ConversationViewSet)

urlpatterns = [
    path('', include(router.urls))
]