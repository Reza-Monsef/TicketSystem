from django.db import models
from django.contrib.auth.models import User
from django.db import models
from .validators import validate_file_size


class Ticket(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='سازنده تیکت')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ساخت تیکت")

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return f"تیکت {self.owner.username}"


class TicketDetail(models.Model):
    user = models.ForeignKey(User, models.CASCADE,
                             verbose_name='فرستنده پیام')
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='ticket_detail', verbose_name='تیکت')
    massage = models.TextField(verbose_name='متن پیام')
    file = models.FileField(null=True, blank=True,
                            upload_to=f'files', validators=[validate_file_size], verbose_name='فایل ضمیمه پیام')

    class Meta:
        verbose_name = 'جزئیات تیکت'
        verbose_name_plural = 'جزئیات تیکت ها'

    def __str__(self) -> str:
        return f"تیکت {self.ticket.title}"

    def status(self):
        if self.user == self.ticket.owner:
            return True
        else:
            return False

    def status_detail(self):
        if self.user == self.ticket.owner:
            return 'پاسخ داده نشده'
        else:
            return 'پاسخ داده شده'

    status_detail.short_description = 'وضعیت تیکت'
