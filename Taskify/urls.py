from django.urls import path
from .views import HomePageView, ProfileUpdateView, handleTask, RegisterView, TaskCreateView, TaskDeleteView, LoginView, LogoutView

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),

    path("task-status/<int:pk>/", handleTask, name='task-status'),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name='task-delete'),
    path("task/create/", TaskCreateView.as_view(), name='task-create'),
    path("profile/<int:pk>/", ProfileUpdateView.as_view(), name='profile-page'),

    path("register/", RegisterView.as_view(), name="register-page"),
    path("login/", LoginView.as_view(), name="login-page"),
    path("logout/", LogoutView.as_view(), name="logout-page"),
]
