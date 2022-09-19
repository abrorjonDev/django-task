from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "fio")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs['class'] = 'form-control p-2'
        self.fields['fio'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['type'] = 'password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['type'] = 'password'




class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control p-2'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control p-2'}))