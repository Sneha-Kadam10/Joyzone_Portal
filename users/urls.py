from django.urls import path
from .views import register, KidLoginView, AdminLoginView, dashboard
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", KidLoginView.as_view(), name="login"),          # Kid login
    path("admin-login/", AdminLoginView.as_view(), name="admin-login"),  # Admin login
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
]
