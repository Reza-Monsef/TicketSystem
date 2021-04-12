from django.db import models
from config.timestampmodel import TimeStampModel

# Create your models here.

#Common users
 

class CommonAccessLevelGroup(TimeStampModel):
    name = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        help_text="",
    )
    ename = models.CharField(
        null=True, 
        blank=True,
        max_length=200,
        help_text=""
    )


class CommonAccessLevel(TimeStampModel):

    common_acceess_level_group = models.ForeignKey(
        CommonAccessLevelGroup,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=""
    )

    ename = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=""
    )

    subject = models.ManyToManyField(
        'access_level.AccessLevelSubject'
    )
    group = models.ManyToManyField(
        'access_level.AccessLevelGroup'
    )
    action = models.ManyToManyField(
        'access_level.AccessLevelAction'
    )