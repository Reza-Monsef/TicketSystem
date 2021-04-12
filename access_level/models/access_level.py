from config.timestampmodel import TimeStampModel
from django.db import models


class AccessLevelSubject(TimeStampModel):

    name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        unique=True
    )

    icon = models.ImageField(
        upload_to='files/AccessLevel/icon',
        null=True,
        blank=True,
        validators=
    )
