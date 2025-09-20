from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Homepage view
def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage
    path('', home, name="home"),

    # Quiz URLs (include from quizzes app)
    path('quizzes/', include("quizzes.urls")),

    # User authentication (register, login, logout)
    path('users/', include("users.urls")),

    # Kid dashboard (after login)
    path('dashboard/', include("dashboard.urls")),
]
