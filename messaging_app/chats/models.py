from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'guest'),
        ('host', 'host'),
        ('admin', 'admin'),
    )
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    #password_hash = models.charfield(max_length=10, blank=False, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices = ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    participants_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_conversations')
    host_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_conversations')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender_id} : {self.message_body}'
