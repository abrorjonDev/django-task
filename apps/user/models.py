from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    email   = models.EmailField("Email", unique=True)
    fio     = models.CharField(max_length=150)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio']

    objects = UserManager()

    class Meta:
        verbose_name        = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.fio