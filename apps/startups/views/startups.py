from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, UpdateView, DetailView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.contrib import messages

from ..models import Startups
from ..forms import StartupsForm, StartupsModelForm, RevenueForm


class HomeView(LoginRequiredMixin, View):
    template_name = "startups/home.html"
    queryset = Startups.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            return self.queryset.filter(created_by=user)
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = dict()
        context["startups"] = self.get_queryset()
        
        return context
    

class StartupCreateView(LoginRequiredMixin, FormView):
    template_name = "startups/_create_form.html"
    form_class = StartupsForm
    success_url = "/"
    def form_valid(self, form):
        name = form.cleaned_data['name']
        try:
            startup = Startups.objects.create(name=name, created_by=self.request.user)
        except IntegrityError:
            messages.add_message(self.request, messages.WARNING, "Bunday nomdagi biznes obyekti mavjud.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs.setdefault('page_title', "Biznes qo'shish")
        kwargs.setdefault('action_name', "Saqlash")

        return super().get_context_data(**kwargs)

class BaseObjectView(LoginRequiredMixin, UserPassesTestMixin):
    model = Startups
    def test_func(self):
        startup = self.get_object()
        return any((startup.created_by==self.request.user, self.request.user.is_superuser))
    
    def get_context_data(self, **kwargs):
        kwargs.setdefault('page_title', self.page_title)
        kwargs.setdefault('action_name', self.action_name)

        return super().get_context_data(**kwargs)

class StartupDetailView(BaseObjectView, DetailView):
    template_name = "startups/_detail.html"
    page_title = "Biznes obyektini hisoblari"
    action_name =  "Tahrirlash"

    def get_context_data(self, **kwargs):
        startup = self.get_object()
        revenues = startup.revenues.all()
        kwargs.setdefault("revenues", revenues)
        kwargs.setdefault("startup", startup)
        kwargs.setdefault("form", RevenueForm())
        return super().get_context_data(**kwargs)
    

class StartupUpdateView(BaseObjectView, UpdateView):
    template_name = "startups/_create_form.html"
    form_class = StartupsModelForm
    success_url = "/"
    page_title = "Biznes obyektini tahrirlash"
    action_name =  "Tahrirlash"