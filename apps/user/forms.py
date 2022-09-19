from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import User

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "fio",)