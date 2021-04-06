from ticket.views import MyTicketList, MyTicketsCreateDetail, TicketList, TicketDetailList, TicketDetailCreate
from django.urls import path, include

app_name = 'ticket'

urlpatterns = [
    # list of tickets
    path('api/tickets', TicketList.as_view(), name='ticket-list'),
    path('api/tickets_detail', TicketDetailList.as_view(),
         name='ticket-detail'),
    path('api/tickets_create', TicketDetailCreate.as_view(),
         name='create-ticket-detail'),
    path('api/mytickets', MyTicketList.as_view(), name='my-ticket-list'),
    path('api/mytickets_create', MyTicketsCreateDetail.as_view(),
         name='my-ticket-create'),
]
