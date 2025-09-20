from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizzes.models import QuizResult


@login_required
def dashboard(request):
    user = request.user
    age_group = getattr(user, "age_group", None)  # safer if user has no age_group

    # ✅ Get quiz progress (latest first)
    results = QuizResult.objects.filter(user=user).order_by("-date_taken")

    # ✅ Suggest activities by age group
    activities = []
    if age_group == "5-7":
        activities = [
            {"name": "Alphabet Game", "icon": "🔤", "url": "#"},
            {"name": "Number Game", "icon": "🔢", "url": "#"},
        ]
    elif age_group == "8-10":
        activities = [
            {"name": "Maths Quiz", "icon": "🧮", "url": "#"},
            {"name": "General Knowledge Quiz", "icon": "🌍", "url": "#"},
            {"name": "English Quiz", "icon": "📚", "url": "#"},
            {"name": "Puzzle Game", "icon": "🧩", "url": "#"},
        ]
    elif age_group == "11-12":
        activities = [
            {"name": "GK Challenge", "icon": "🎯", "url": "#"},
            {"name": "Logic Game", "icon": "🧠", "url": "#"},
            {"name": "Beginner Coding", "icon": "💻", "url": "#"},
        ]

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "age_group": age_group,
            "activities": activities,
            "results": results,   # ✅ Pass quiz history to template
        },
    )
