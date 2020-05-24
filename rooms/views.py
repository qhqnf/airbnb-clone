from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    context_object_name = "rooms"
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
