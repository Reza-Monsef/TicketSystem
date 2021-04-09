from django.urls import path, re_path
from ticket.views import (AllAcounts, ListTickets,
                          MyAcount, MyTicketList,
                          MyTicketsCreateDetail, MyUploadView, TicketList,
                          TicketDetailList, TicketDetailCreate
                          )

app_name = 'ticket'

urlpatterns = [
    path('api/upload', MyUploadView.as_view()),
    path('api/AllAcounts', AllAcounts.as_view(), name='ticket-AllAcounts'),
    path('api/MyAcount', MyAcount.as_view(), name='ticket-MyAcount'),
    path('api/tickets', TicketList.as_view(), name='ticket-list'),
    path('api/tickets2', ListTickets.as_view(), name='ticket-list2'),
    path('api/tickets_detail', TicketDetailList.as_view(),
         name='ticket-detail'),
    path('api/tickets_create', TicketDetailCreate.as_view(),
         name='create-ticket-detail'),
    path('api/mytickets', MyTicketList.as_view(), name='my-ticket-list'),
    path('api/mytickets_create', MyTicketsCreateDetail.as_view(),
         name='my-ticket-create'),
]
