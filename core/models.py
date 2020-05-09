from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stameped Model """

    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        abstract = True
