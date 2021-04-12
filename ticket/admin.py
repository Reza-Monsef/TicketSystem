from django.contrib import admin
from .models import Ticket, Message
# Register your models here.

admin.site.site_header = 'تیکت سایت'


class MessageAdmin(admin.ModelAdmin):
    pass 


admin.site.register(Ticket)
admin.site.register(Message, MessageAdmin)
