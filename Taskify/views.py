from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


class HomePageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"
    login_url = reverse_lazy("login-page")


class RegisterView(generic.CreateView):
    template_name = 'register.html'
    queryset = User.objects.all()
    form_class = RegisterForm
    success_url = reverse_lazy("login-page")

    def get_success_url(self) -> str:
        return self.success_url

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home-page"))
        return super().get(request, *args, **kwargs)


class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy("home-page")

    def get_success_url(self) -> str:
        return self.success_url

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_redirect_url(self) -> str:
        return super().get_redirect_url()


class LogoutView(LogoutView):
    next_page = reverse_lazy("login-page")


"""
    1. Tasks
    - Display tasks
    - Create tasks
    - Update tasks
    - Delete tasks

    2. Profile
    - Update profile data
    - Delete profile

    3. Auth
    - Login
    - Register
"""
