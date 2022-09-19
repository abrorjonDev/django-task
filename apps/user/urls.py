from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import SignUpView, LoginView

app_name = "user"
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="signup"),
    path('sign-in/', LoginView.as_view(), name="login"),
    path('sign-out/', LogoutView.as_view(), name="logout"),
    
]