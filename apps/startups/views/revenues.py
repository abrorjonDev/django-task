from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseNotFound

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.views import View
from django.views.generic import UpdateView, DetailView, DeleteView

from apps.startups.views.startups import BaseObjectView
from ..models import Revenues, RevenueFields, Startups
from ..forms import RevenueForm, FieldForm, RevenueModelForm


class RevenueView(LoginRequiredMixin, View):
    model = Revenues
    template_name = "startups/_detail.html"
    form_class = RevenueForm

    def get(self, request, startup_id, *args, **kwargs):
        
        context = self.get_context_data(startup_id=startup_id)
        return render(request, self.template_name, context)
    
    def post(self, request, startup_id, *args, **kwargs):
        form = self.form_class(request.POST)
        context = self.get_context_data(startup_id=startup_id)

        if form.is_valid():
            form.save(startup=self.get_startup(startup_id), request=request)
        
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        startup = self.get_startup(kwargs['startup_id'])

        revenues = startup.revenues.all()
        kwargs.setdefault("revenues", revenues)
        kwargs.setdefault("startup", startup)
        form = self.form_class()
        kwargs.setdefault("form", form)
        return kwargs

    def get_startup(self, startup_id: int):
        startup = get_object_or_404(Startups, pk=startup_id)

        if startup.created_by == self.request.user or self.request.user.is_superuser:
            return startup
        else:
            return HttpResponseNotFound("Bunday object mavjud emas")


class RevenueUpdateView(BaseObjectView, UpdateView):
    template_name = "startups/_create_form.html"
    success_url = "/"
    model = Revenues
    page_title = "Hisobotni Tahrirlash"
    action_name = "Tahrirlash"
    form_class = RevenueModelForm


class RevenueDeleteView(BaseObjectView, DeleteView):
    template_name = "startups/_delete_form.html"
    model = Revenues
    success_url = "/"
    page_title = "Hisobotni O'chirish"
    action_name = "O'chirish"


class RevenueFieldCreateView(LoginRequiredMixin, View):
    template_name = "startups/_create_form.html"
    model = RevenueFields
    form_class = FieldForm

    def get(self, request, revenue_id, *args, **kwargs):
        
        context = self.get_context_data(revenue_id=revenue_id)
        return render(request, self.template_name, context)
    
    def post(self, request, revenue_id, *args, **kwargs):
        form = self.form_class(request.POST)
        context = self.get_context_data(revenue_id=revenue_id)

        if form.is_valid():
            revenue = self.get_revenue(revenue_id)
            form.save(revenue=revenue, request=request)
            messages.add_message(request, messages.INFO, "Soha yaratildi")
            return redirect("startups:startup_detail", pk = revenue.startup.id)
        else:
            messages.add_message(request, messages.DANGER, "Soha qiymatlari bilan bog'liq muammo yuzaga keldi, tekshiring")
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = dict()

        revenue = self.get_revenue(kwargs['revenue_id'])
        context['revenue'] = revenue
        context["page_title"] = "Hisobot sohasini yaratish"
        context['action_name'] = "Yaratish"
        context['form'] = self.form_class()

        return context
    
    def get_revenue(self, revenue_id: int):
        revenue = get_object_or_404(Revenues, pk=revenue_id)

        if revenue.created_by == self.request.user or self.request.user.is_superuser:
            return revenue
        return HttpResponseNotFound("Bunday object mavjud emas")