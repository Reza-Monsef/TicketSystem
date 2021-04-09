
from PIL import Image
from django.http.response import Http404
from rest_framework.views import APIView
from ticket.serializer import TicketDetailSerializer, TicketSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Ticket, TicketDetail
from django.contrib.auth.models import User
from rest_framework.views import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser


class MyUploadView(APIView):
    parser_class = (FileUploadParser,)

    def put(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']

        try:
            img = Image.open(f)
            img.verify()
        except:
            raise ParseError("Unsupported image type")

        id = request.kwargs.get('id')
        TicketDetail.objects.filter(id=id).update(file=f)
        return Response(status=201)


# new
class AllAcounts(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, format=None):
        response = []
        user = User.objects.all()
        for i in user:
            response.append({
                "username": i.username,
                "email": i.email,
                "message": f"کاربر {i.username} مجموعا برای ما {i.tickets.count()} تیکت ثبت کرده است"
            })
        return Response(response)
# new


class MyAcount(APIView):
    def get(self, request, format=None):
        response = []
        user = self.request.user
        myuser = User.objects.get(id=user.id)
        count = myuser.tickets.count()
        response.append({
            "email": myuser.email,
            "message": f"کاربر {myuser.username} شما مجموعا برای ما {count} تیکت ثبت کردید"
        })
        return Response(response)


class TicketList(ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminUser, )


# new
class ListTickets(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        response = []
        for i in Ticket.objects.all():
            response.append({
                "id": i.id,
                "title": i.title
            })
        return Response(response)


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
