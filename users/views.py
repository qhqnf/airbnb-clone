import os
import requests
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import escape_uri_path
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


def build_url_with_query(origin_url: str, **params) -> str:
    """
    Builds an URL with query string for the GET requesting method.
    """
    mapped_params = map(
        lambda k: f"{escape_uri_path(k)}={escape_uri_path(params[k])}", params
    )
    result_url = origin_url.rstrip("?") + "?" + "&".join(mapped_params)
    return result_url


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8001/users/login/github/callback"
    scopes = [
        "read:user",
        "user:email",
    ]
    endpoint = build_url_with_query(
        "https://github.com/login/oauth/authorize",
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=" ".join(scopes),
    )
    return redirect(endpoint)


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = result.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = result_json.get("access_token")
                api_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = api_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name") or ""
                    email = profile_json.get("email") or ""
                    bio = profile_json.get("bio") or ""
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))
