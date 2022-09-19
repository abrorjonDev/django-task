from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseNotFound

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.views import View
from django.views.generic import UpdateView, DetailView, DeleteView

from apps.startups.views.startups import BaseObjectView
from ..models import Revenues, RevenueFields, Startups
from ..forms import RevenueForm, FieldForm


class AdminRevenueView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "startups/admin.html"
    model = Startups

    def get_queryset(self, ):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        context = dict()
        context["startups"] = self.get_queryset() 
        return render(request, self.template_name, context)
    


    def test_func(self):
        return self.request.user.is_superuser
