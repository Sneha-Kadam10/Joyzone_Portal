from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser   # ✅ use your CustomUser model


class KidSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser   # ✅ not default User
        fields = ["username", "age_group", "password1", "password2"]
        labels = {
            "username": "Kid’s Username",
            "age_group": "Select Age Group",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # 🚫 Ensure kids are not admins/staff
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user
