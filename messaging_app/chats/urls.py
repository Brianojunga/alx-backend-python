from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ConversationViewset


router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversation', ConversationViewset)

urlpatterns = [
    path('', include(router.urls))
]