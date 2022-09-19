from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import User



class SignUpView(CreateView):
    """ User Register View"""
    template_name = "user/create_form.html"

    model = User
    success_url = "/"
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        kwargs.setdefault("page_title", "Registration")
        kwargs.setdefault("action_name", "Register")
        kwargs.setdefault("button_tag", "primary")
        return super().get_context_data(**kwargs)


class LoginView(FormView):
    template_name = "user/create_form.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        user = authenticate(self.request,
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password')  
        )
        print(user)
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, "Tizimga muvaffaqiyatli kirdingiz.")
            if user.is_superuser:
                self.success_url = "/admin/"
        else:
            messages.add_message(self.request, messages.WARNING, "Email va parol to'g'ri yozilganligiga ahamiyat bering.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs.setdefault("page_title", "Login")
        kwargs.setdefault("action_name", "Login")
        kwargs.setdefault("button_tag", "primary")
        return super().get_context_data(**kwargs)