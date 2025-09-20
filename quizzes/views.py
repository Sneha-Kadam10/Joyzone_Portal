from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizResult
from django.utils import timezone


@login_required
def quiz_list(request):
    user = request.user

    # If kid (not admin), show only their age group quizzes
    if not user.is_superuser:
        if hasattr(user, "age_group"):  # ensure CustomUser has this field
            quizzes = Quiz.objects.filter(age_group=user.age_group, is_published=True)
        else:
            quizzes = Quiz.objects.none()
    else:
        # Admin sees nothing here, redirect to admin panel
        return redirect("/admin/")

    return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Restrict kids to their own age group
    if not request.user.is_superuser and request.user.age_group:
        if quiz.age_group != request.user.age_group:
            return redirect("quiz_list")

    questions = quiz.question_set.all()

    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected and int(selected) == q.correct_option:
                score += 1

        # ✅ Save attempt
        result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=questions.count(),
            date_taken=timezone.now()  # ✅ force date to save
        )

        # Redirect to result page
        return redirect("quiz_result", result_id=result.id)

    return render(request, "quizzes/take_quiz.html", {"quiz": quiz, "questions": questions})


@login_required
def quiz_result(request, result_id):
    """Show the result of a completed quiz"""
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    return render(request, "quizzes/result.html", {"result": result})
