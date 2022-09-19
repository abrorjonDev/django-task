from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegistrationView

app_name = "user"

urlpatterns = [
    path("signup/", RegistrationView.as_view(), name="sign-up"),
    
    path('login/', LoginView.as_view(template_name="user/login.html"), name="sign-in"),
    path('logout/', LogoutView.as_view(), name="sign-out"),
]
