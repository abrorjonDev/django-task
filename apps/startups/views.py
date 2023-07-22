from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseForbidden
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.db.models import Q

from typing import Dict, Any
from .models import Revenues, Startups, Outgoings
from .forms import StartupForm, RevenueForm, OutgoingForm
from apps.user.models import User
# Create your views here.



class HomeView(LoginRequiredMixin, ListView):
    template_name = "startups/home.html"

    def get_queryset(self):
        queryset = Startups.objects.all()
        user = self.request.user
        if user.is_superuser:
            return queryset
        admins = User.objects.filter(is_superuser=True)
        return queryset.filter(Q(author=user) | Q(author__in=admins))

    def get_context_data(self, **kwargs):
        kwargs.setdefault("page_title", "Biznes Loyihalar")
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.template_name = "startups/vc_index.html"
        return super().get(request, *args, **kwargs)

def startup_create(request):
    kwargs = {
        "page_title": "LOYIHA YARATISH",
        "action_name": "Jo'natish",
        "button_tag": "primary"
    }

    if request.method == "POST":
        form = StartupForm(request.POST)
        if form.is_valid():
            startup = form.save(commit=False)
            startup.author = request.user
            startup.save()

            return redirect("/")
    else:
        form = StartupForm()
    kwargs.setdefault("form", form)
    return render(request, "user/create_form.html", kwargs)

class StartupDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "startups/detail.html"
    model = Startups

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["categories"] = self.get_revenue_categories()
        return super().get_context_data(**kwargs)
    
    def get_revenue_categories(self):
        return get_list_or_404(Revenues, startup=self.get_object())


class StartupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "user/create_form.html"
    model = Startups
    form_class = StartupForm
    success_url = "/"

    def get_success_url(self) -> str:
        messages.add_message(self.request, messages.SUCCESS, "Muvaffaqiyatli yangilandi")
        # if self.request.user.is_superuser:
        #     self.success_url = "/admin/"
        return super().get_success_url()
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs.update({
            "page_title": "LOYIHA TAHRIRLASH",
            "action_name": "Jo'natish",
            "button_tag": "primary"
        })
        return super().get_context_data(**kwargs)
    
    def test_func(self):
        return self.get_object().author == self.request.user


class StartupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "startups/delete_form.html"
    model = Startups
    success_url = "/"

    def get_success_url(self) -> str:
        messages.add_message(self.request, messages.SUCCESS, "Muvaffaqiyatli o'chirildi")
        # if self.request.user.is_superuser:
        #     self.success_url = "/admin/"
        return super().get_success_url()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("page_title", "LOYIHANI O'CHIRISH")
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.get_object().author == self.request.user


class ReportListView(LoginRequiredMixin, ListView):
    template_name = "startups/report_detail.html"
    startup = None

    def get_queryset(self):
        queryset = Revenues.objects.all()
        kwargs = {"startup": self.startup}
        if not self.request.user.is_superuser:
            kwargs["author"] = self.request.user
        return queryset.filter(**kwargs).order_by("-date_created")

    def get(self, request, *args, **kwargs):
        self.startup = get_object_or_404(Startups, pk=kwargs["startup_id"])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        kwargs = {"startup": self.startup}
        if not self.request.user.is_superuser:
            kwargs["author"] = self.request.user

        outgoings = Outgoings.objects.filter(**kwargs).order_by("-date_created")

        kwargs.update({
            "outgoings": outgoings,
            "startup": self.startup
        })
        return super().get_context_data(**kwargs)


def check_availability(request, startup_id: int):
    startup = get_object_or_404(Startups, pk=startup_id)
    if request.user.is_superuser:
        raise Http404
    if not request.user.is_superuser and startup.author != request.user and not startup.author.is_superuser:
        raise Http404
        # messages.add_message(request, messages.WARNING, "Sizga mumkinmas")
        # return redirect("startups:reports", startup_id=startup_id)


def report_create(request, startup_id: int):
    check_availability(request, startup_id)
    
    if request.method == "POST":
        form = RevenueForm(request.POST)
        if form.is_valid():
            income = form.cleaned_data.get("income")
            clients = form.cleaned_data.get("clients")

            last_revenue = Revenues.objects.filter(startup_id=startup_id, author=request.user).last() # filtered on -date_created
            
            revenue = Revenues(
                income=income, clients=clients, startup_id=startup_id, author=request.user
            )
            try:
                revenue.percentage = (income - last_revenue.income) / last_revenue.income * 100
            except:
                pass
            if revenue.percentage < 0:
                revenue.is_rising = False

            try:
                revenue.client_percentage = (clients- last_revenue.clients) / last_revenue.clients * 100
            except:
                pass
            if revenue.client_percentage < 0:
                revenue.client_rising = False
            revenue.save()
            return redirect("startups:reports", startup_id=startup_id)
    else:
        form = RevenueForm() 
    
    return render(request, "startups/revenue_add.html", {"form": form})


def expense_create(request, startup_id: int):
    check_availability(request, startup_id)
    if request.method == "POST":
        form = OutgoingForm(request.POST)
        if form.is_valid():
            salary = form.cleaned_data.get("salary")
            marketing = form.cleaned_data.get("marketing")

            last_expense = Outgoings.objects.filter(startup_id=startup_id, author=request.user).last() # filtered on -date_created
            
            expense = Outgoings(
                salary=salary, marketing=marketing, startup_id=startup_id, author=request.user
            )
            try:
                expense.percentage = (salary - last_expense.salary)/ last_expense.salary * 100 
            except:
                pass
            if expense.percentage < 0:
                expense.is_rising = False
            
            try:
                expense.marketing_percentage = (marketing - last_expense.marketing)/ last_expense.marketing * 100
            except:
                pass
            if expense.marketing_percentage < 0:
                expense.marketing_rising = False

            expense.save()
            return redirect("startups:reports", startup_id=startup_id)
    else:
        form = OutgoingForm() 
    
    return render(request, "startups/expense_add.html", {"form": form})
