from django.shortcuts import render
from django.views.generic import CreateView

from .forms import RegistrationForm



class RegistrationView(CreateView):
    template_name = "user/registration.html"

    form_class = RegistrationForm
    success_url = '/login/'