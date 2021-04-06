from django.contrib import admin
from .models import Ticket, TicketDetail
# Register your models here.

admin.site.site_header = 'تیکت سایت'


class TicketDetailAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'ticket', 'user', 'status_detail')


admin.site.register(Ticket)
admin.site.register(TicketDetail, TicketDetailAdmin)
