from django.db.models import fields
from rest_framework import serializers
from .models import Ticket, Message


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
