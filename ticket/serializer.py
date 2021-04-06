from django.db.models import fields
from rest_framework import serializers
from .models import Ticket, TicketDetail


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'title',)


class TicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDetail
        fields = ('ticket', 'massage', 'file')
