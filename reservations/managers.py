from django.db import models


class CustomReservationManager(models.manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.models.DoesNotExist:
            return None
