from django.urls import path
from .views import HomePageView, RegisterView, LoginView, LogoutView
urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),


    path("register/", RegisterView.as_view(), name="register-page"),
    path("login/", LoginView.as_view(), name="login-page"),
    path("logout/", LogoutView.as_view(), name="logout-page"),
]
