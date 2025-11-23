import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages sent after a timestamp
    sent_after = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    # Filter messages sent before a timestamp
    sent_before = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    # Filter by sender
    sender = django_filters.CharFilter(
        field_name="sender_id__user_id",
        lookup_expr="exact"
    )

    class Meta:
        model = Message
        fields = ['sender', 'sent_after', 'sent_before']
