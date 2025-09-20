from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import KidSignUpForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = KidSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # ✅ Ensure only kids (not admins) register here
            user.is_staff = False
            user.is_superuser = False
            user.save()

            login(request, user)  # auto-login after signup
            return redirect("dashboard")  # redirect to kid’s dashboard
    else:
        form = KidSignUpForm()
    return render(request, "users/register.html", {"form": form})


# 🔹 Kid Login View
class KidLoginView(LoginView):
    template_name = "users/login.html"
    extra_context = {"login_type": "kid"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_title"] = "Kid Login"
        return context

    def form_valid(self, form):
        """ Prevent staff/admin from logging in via Kid login page """
        user = form.get_user()
        if user.is_staff or user.is_superuser:
            messages.error(self.request, "Admins must use the Admin Login page.")
            return redirect("admin-login")   # ✅ fixed name
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard")


# 🔹 Admin Login View
class AdminLoginView(LoginView):
    template_name = "users/admin_login.html"
    extra_context = {"login_type": "admin"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_title"] = "Admin Login"
        return context

    def form_valid(self, form):
        """ Prevent kids from logging in via Admin login page """
        user = form.get_user()
        if not (user.is_staff or user.is_superuser):
            messages.error(self.request, "Kids must use the Kid Login page.")
            return redirect("login")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin:index")


@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")
