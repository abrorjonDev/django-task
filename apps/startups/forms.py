from django import forms


from .models import Startups, Revenues


class StartupForm(forms.ModelForm):
    class Meta:
        model = Startups
        fields = ("name", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'


class RevenueForm(forms.Form):

    income = forms.IntegerField()
    clients = forms.IntegerField()


class OutgoingForm(forms.Form):

    salary = forms.IntegerField()
    marketing = forms.IntegerField()