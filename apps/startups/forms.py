from django.db import IntegrityError
from django import forms
from django.contrib import messages
from apps.user.models import User
from .models import Startups, Revenues, RevenueFields

class StartupsForm(forms.Form):
    name = forms.CharField(
        label="Biznes nomi",required=True, max_length=120,
        widget=forms.TextInput(attrs={'class':"form-control p-2 m-2"})
    )

    # class Meta:
    #     model = Startups
    #     fields = ("name",)

class StartupsModelForm(forms.ModelForm):
    name = forms.CharField(
        label="Biznes nomi",required=True, max_length=120,
        widget=forms.TextInput(attrs={'class':"form-control p-2 m-2"})
    )

    class Meta:
        model = Startups
        fields = ("name",)

class RevenueModelForm(forms.ModelForm):
    class Meta:
        model = Revenues
        fields = ("name", "startup")

    def __init__(self, *args, **kwargs):
        super(RevenueModelForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control m-auto'
        self.fields['startup'].widget.attrs['class'] = 'form-control m-auto'



class RevenueForm(forms.Form):
    name = forms.CharField(
        label="Hisobot nomi",required=True, max_length=120,
        widget=forms.TextInput(attrs={'class':"form-control p-2 m-2"})
    )

    def save(self, startup: Startups, request, *args, **kwargs):
        revenue = Revenues(
            name=self.cleaned_data.get('name'), 
            startup=startup, created_by=request.user)
        try:
            revenue.save()
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "Bunday nomdagi hujjat yaratilgan.")
            return forms.ValidationError("Bunday nomdagi hujjat yaratilgan.")
        
        return revenue


class FieldForm(forms.Form):
    name = forms.CharField(
        label="Hisobot nomi",required=True, max_length=120,
        widget=forms.TextInput(attrs={'class':"form-control p-2 m-2"})
    )

    value = forms.IntegerField(
        label="Soha qiymati", required=True,
        widget=forms.NumberInput(attrs={'class':"form-control p-2 m-2"})
    )

    def save(self, revenue: Revenues, request, *args, **kwargs):
        value=self.cleaned_data.get('value')
        name=self.cleaned_data.get('name')

        try:
            field = RevenueFields.objects.get(
                name=name, revenue=revenue, created_by=request.user)
        except:
            field = RevenueFields.objects.create(
                name=name, revenue=revenue, created_by=request.user
            )

        if field.value > value:
            field.is_plus = False
        if field.value:
            field.percentage = value / field.value * 100
        else:
            field.percentage = 100.0
        field.value = value
        field.save(update_fields=['value', 'percentage', 'is_plus'])

        return revenue