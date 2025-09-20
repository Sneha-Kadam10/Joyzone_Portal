from django.db import models
from django.conf import settings



class Quiz(models.Model):
    SUBJECT_CHOICES = [
        ("Maths", "Maths"),
        ("GK", "General Knowledge"),
        ("English", "English"),
    ]

    AGE_GROUP_CHOICES = [
        ("5-7", "5–7 Years"),
        ("8-10", "8–10 Years"),
        ("11-12", "11–12 Years"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES)
    difficulty = models.CharField(
        max_length=20,
        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
        default="Easy"
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject}, {self.age_group})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(
        choices=[(1, "Option 1"), (2, "Option 2"), (3, "Option 3"), (4, "Option 4")]
    )

    def __str__(self):
        return self.text


class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        return (self.score/ self.total_questions) * 100 if self.total_questions > 0 else 0
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: ({self.score}/{self.total_questions})"
