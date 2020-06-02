import os
import requests
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):

    """ LoginView Definition """

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SingUpForm
    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "hyunchul",
        "last_name": "yang",
        "email": "example@gmail.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error Message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8001/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    client_id = os.environ("GITHUB_ID")
    client_secret = os.environ("GITHUB_SECRET")
    code = request.GET.get("code", None)
    if code is not None:
        request = requests.POST(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        print(request.json())
    return redirect(reverse("core:home"))
