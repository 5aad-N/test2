from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """User registration form with custom fields: email, DOB, profile image."""

    class Meta:
        model = User
        fields = ("username", "email", "date_of_birth", "profile_image")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "name@example.com"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "profile_image": forms.FileInput(attrs={"class": "form-control"}),
        }
