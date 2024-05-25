from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Task, Profile
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .filters import TaskFilter


class HomePageView(LoginRequiredMixin, FilterView):
    template_name = "home.html"
    login_url = reverse_lazy("login-page")
    filterset_class = TaskFilter

    def get_queryset(self) -> QuerySet[Any]:
        user_tasks = Task.objects.filter(profile__user=self.request.user)
        return user_tasks


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'profile.html'
    form_class = ProfileUpdateForm
    login_url = reverse_lazy("login-page")

    def get_success_url(self) -> str:
        return reverse_lazy('profile-page', kwargs={"pk": Profile.objects.get(user=self.request.user).id})

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get_initial(self) -> dict[str, Any]:
        profile = Profile.objects.get(user=self.request.user)
        initial = super().get_initial()
        initial['avatar'] = profile.avatar
        return initial


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    success_url = reverse_lazy("home-page")
    template_name = 'create.html'
    fields = ['title', 'description', 'priority']
    login_url = reverse_lazy("login-page")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        try:
            form.instance.profile = Profile.objects.get(user=self.request.user)
            return super().form_valid(form)
        except Profile.DoesNotExist:
            messages.error(self.request, "Profile doesn't exists")
            return redirect('logout-page')


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("home-page")

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(request, "task deleted")
        return super().delete(request, *args, **kwargs)


@login_required
def handleTask(request, pk):
    if request.method == "POST":
        try:
            task = Task.objects.get(id=pk)
            if task.status:
                task.status = False
                task.save()
                messages.success(request, f"""Changed task#{
                                 task.id}  status for completed""")
            else:
                task.status = True
                task.save()
                messages.success(request, f"""Changed task#{
                                 task.id}  status for uncomplted""")
            return redirect("home-page")
        except Task.DoesNotExist:
            messages.error(request, "Task doesn't exists")
            return redirect("home-page")


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
