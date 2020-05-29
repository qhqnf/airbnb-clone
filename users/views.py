from django.shortcuts import render
from django.views import View
from . import forms


class LoginView(View):

    """ LoginView Definition """

    def get(self, request):

        form = forms.LoginForm(initial={"email": "example@gmail.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        return render(request, "users/login.html", {"form": form})
