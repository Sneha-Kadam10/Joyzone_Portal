from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    AGE_GROUP_CHOICES = [
        ('5-7', '5–7 Years'),
        ('8-10', '8–10 Years'),
        ('11-12', '11–12 Years'),
    ]

    age_group = models.CharField(
        max_length=10,
        choices=AGE_GROUP_CHOICES,
        null=True,
        blank=True,
        help_text="Select the child’s age group"
    )

    def __str__(self):
        return f"{self.username} ({self.age_group})" if self.age_group else self.username
