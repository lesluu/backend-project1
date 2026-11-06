from rest_framework import serializers
from .models import Ticket, Reply


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'status']


class ReplySerializer(serializers.ModelSerializer):
    ticket_id = serializers.IntegerField(source='ticket.id', read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'ticket_id', 'author', 'text', 'created_at']
        read_only_fields = ['ticket_id', 'created_at']