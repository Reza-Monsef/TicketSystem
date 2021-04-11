from django.db import models
from django.contrib.auth.models import User
from django.db import models
from .validators import validate_file_size
from config.timestampmodel import TimeStampModel


def validate_file(myfile):
    file_size = myfile.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
       raise ValidationError("Max size of file is %s MB" % limit_mb)


def message_file_path(instance, filename):
    return 'user_{}/tickets/ticket_{}/{}'.format(instance.message.ticket.customer.id, instance.message.ticket.id ,filename)


# class Ticket(models.Model):
#     title = models.CharField(max_length=250, verbose_name='عنوان')
#     owner = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name='سازنده تیکت', related_name='tickets')
#     created_at = models.DateTimeField(
#         auto_now_add=True, verbose_name="زمان ساخت تیکت")

#     class Meta:
#         verbose_name = 'تیکت'
#         verbose_name_plural = 'تیکت ها'

#     def __str__(self):
#         return f"تیکت {self.owner.username}"


class Ticket(TimeStampModel):

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
        )

    subject = models.CharField(max_length=250)
    
    answered = models.BooleanField(
        default=False, 
        blank=True, 
        help_text="",
    )
    
    seen_by_coustomer = models.BooleanField(
        default=True
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        blank=True,
        null=True,
        related_name="assigned_to",
    )

     class Meta:
         verbose_name = 'تیکت'
         verbose_name_plural = 'تیکت ها'
    
    def __str__(self):
        return f"تیکت {self.owner.username}"


# class TicketDetail(models.Model):
#     user = models.ForeignKey(User, models.CASCADE,
#                              verbose_name='فرستنده پیام', related_name='tickets_detail')
#     ticket = models.ForeignKey(
#         Ticket, on_delete=models.CASCADE, related_name='ticket_detail', verbose_name='تیکت')
#     massage = models.TextField(verbose_name='متن پیام')
#     file = models.FileField(null=True, blank=True,
#                             upload_to=f'files', validators=[validate_file_size], verbose_name='فایل ضمیمه پیام')

#     class Meta:
#         verbose_name = 'جزئیات تیکت'
#         verbose_name_plural = 'جزئیات تیکت ها'

#     def __str__(self) -> str:
#         return f"تیکت {self.ticket.title}"

#     def status(self):
#         if self.user == self.ticket.owner:
#             return True
#         else:
#             return False

#     def status_detail(self):
#         if self.user == self.ticket.owner:
#             return 'پاسخ داده نشده'
#         else:
#             return 'پاسخ داده شده'

#     status_detail.short_description = 'وضعیت تیکت'


class Message(TimeStampModel):

    swnder = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='ticket_detail',
        verbose_name='فرستنده پیام'
    )
    
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ticket_detail'
    )

    text_content = models.TextField(
        blank=True,
        null=True
    )

    file_attach = models.BooleanField(
        default=False
    )


class MessageFile(TimeStampModel):

    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )

    file_content = models.FileField(
        upload_to=message_file_path,
        validators=[
            validate_file            
        ]
        
    )