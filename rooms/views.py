from django.utils import timezone
from django.views.generic import ListView
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    context_object_name = "rooms"
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        now = timezone.now()
        context["now"] = now
        return context
