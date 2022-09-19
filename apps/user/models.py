from django.db import models
from django.contrib.auth.models import AbstractUser


from .managers import CustomUserManager

class User(AbstractUser):
    username = first_name = last_name = None
    
    email = models.EmailField("Email", unique=True)
    fio = models.CharField("User full_name", max_length=150)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS = ['fio']

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        abstract = False

