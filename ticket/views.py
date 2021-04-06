from django.core.exceptions import ValidationError
from django.http.response import Http404
from ticket.serializer import TicketDetailSerializer, TicketSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Ticket, TicketDetail
from .permissions import IsOwner

# Create your views here.


class TicketList(ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminUser, )


class TicketDetailList(ListAPIView):
    serializer_class = TicketDetailSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return TicketDetail.objects.all()


class TicketDetailCreate(CreateAPIView):
    serializer_class = TicketDetailSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return TicketDetail.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyTicketList(ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyTicketsCreateDetail(CreateAPIView):
    serializer_class = TicketDetailSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        tickett = self.request.data['ticket']
        ticket = Ticket.objects.filter(id=tickett).first()
        print(ticket.owner)
        if ticket.owner == self.request.user:
            serializer.save(user=self.request.user)
        else:
            raise Http404("شما دسترسی به این تیکت ندارید")
