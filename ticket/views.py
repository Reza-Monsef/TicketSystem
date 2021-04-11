
from PIL import Image
from django.http.response import Http404
from rest_framework.views import APIView
from ticket.serializer import MessageSerializer, TicketSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.views import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.authentication import TokenAuthentication
from .models import Ticket, Message

# # new
# class AllAcounts(APIView):
#     permission_classes = (IsAdminUser, )

#     def get(self, request, format=None):
#         response = []
#         user = User.objects.all()
#         for i in user:
#             response.append({
#                 "username": i.username,
#                 "email": i.email,
#                 "message": f"کاربر {i.username} مجموعا برای ما {i.tickets.count()} تیکت ثبت کرده است"
#             })
#         return Response(response)
# # new


# class MyAcount(APIView):
#     def get(self, request, format=None):
#         response = []
#         user = self.request.user
#         myuser = User.objects.get(id=user.id)
#         count = myuser.tickets.count()
#         response.append({
#             "email": myuser.email,
#             "message": f"کاربر {myuser.username} شما مجموعا برای ما {count} تیکت ثبت کردید"
#         })
#         return Response(response)


# class TicketList(ListCreateAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     permission_classes = (IsAdminUser, )


# # new
# class ListTickets(APIView):
#     permission_classes = (IsAuthenticated, )

#     def get(self, request, format=None):

#         ticket_objs = Ticket.objects.first()


#         ticket_serialized = TicketSerializer(
#             ticket_objs,
#         )

#         TicketSerializer(
#             data=request.data
#         )

#         TicketSerializer(
#             ticket_objs,
#             data=request.data,
#             partial=True
#         )


#         response_json = {
#             'succeeded': True,
#             'tickets': ticket_serialized.data
#         }



#         response = []
#         for i in Ticket.objects.all():
#             response.append({
#                 "id": i.id,
#                 "title": i.title
#             })
#         return Response(response)


# class TicketDetailList(ListAPIView):
#     serializer_class = TicketDetailSerializer
#     permission_classes = (IsAdminUser, )

#     def get_queryset(self):
#         return TicketDetail.objects.all()


# class TicketDetailCreate(CreateAPIView):
#     serializer_class = TicketDetailSerializer
#     permission_classes = (IsAdminUser, )

#     def get_queryset(self):
#         return TicketDetail.objects.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class MyTicketList(ListCreateAPIView):
#     serializer_class = TicketSerializer
#     permission_classes = (IsAuthenticated, )

#     def get_queryset(self):
#         user = self.request.user
#         return Ticket.objects.filter(owner=user)

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class MyTicketsCreateDetail(CreateAPIView):
#     serializer_class = TicketDetailSerializer
#     permission_classes = (IsAuthenticated,)

#     def perform_create(self, serializer):
#         tickett = self.request.data['ticket']
#         ticket = Ticket.objects.filter(id=tickett).first()
#         print(ticket.owner)
#         if ticket.owner == self.request.user:
#             serializer.save(user=self.request.user)
#         else:
#             raise Http404("شما دسترسی به این تیکت ندارید")



def existence_error(object_name):
    return Response(
        {
            'succeeded': False,
            'details': '{} object does not exist!'.format(object_name),
            'error_type': 'existence_error'
        },
        status=404
    )


def validation_error(serialized):
    return Response(
        {
            'succeeded': False,
            'details': serialized.errors,
            'error_type': 'validation_error'
        },
        status=400
    )




class TicketCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        request.data.update({"owner":request.user})

        ticket_serialized = TicketSerializer(
            data=request.data,
        )

        if not ticket_serialized.is_valid():
            raise validation_error(ticket_serialized)
        
        ticket_serialized.save()

        response_json = {
            "succeded":True,
            "ticket":ticket_serialized.data
        }
        return Response(response_json, status=200)


class TicketAPIView(APIView):
    authentication_classes=(TokenAuthentication, )
    permission_classes=(IsAuthenticated, )

    def post(self, request):

        ticket_obj = Ticket.objects.filter(id=request.data.get('id'), coustomer=request.user.id).first()

        if ticket_obj is None:
            return existence_error("ticket")

        ticket_serialized = TicketSerializer(
            ticket_obj,
            data={
                "seen_by_customer":True,
            },
            partial=True
        )
        if is not ticket_serialized.is_valid():
            return validation_error(ticket_serialized)
        ticket_serialized.save()

        message_obj = Message.objects.filter(ticket=ticket_obj.id).order_by('-id')

        message_serialized = MessageSerializer(message_obj, many=True)

        json_response = {
            "succeded":True,
            "ticket":ticket_serialized.data,
            "message":message_serialized.data
        }
        return Response(data=json_response, status=200)