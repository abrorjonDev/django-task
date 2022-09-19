from django.db import models
from django.urls import reverse

from apps.user.models import User

# Create your models here.

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.CASCADE, related_name='+')

    class Meta:
        abstract = True
        ordering = ("date_created", )

    def __str__(self):
        return self.name


class Startups(BaseModel):
    name = models.CharField("Biznes nomi", unique=True, max_length=120)

    class Meta(BaseModel.Meta):
        abstract = False
        verbose_name = "Start up"
        verbose_name_plural = "Start up"

    # def get_absolute_url(self):
    #     return reverse_lazy("model_detail", kwargs={"pk": self.pk})
    

class Revenues(BaseModel):
    name = models.CharField("Hisobot nomi", max_length=120)

    startup = models.ForeignKey(Startups, models.CASCADE, verbose_name="Biznes",
                                related_name="revenues")

    class Meta(BaseModel.Meta):
        abstract = False
        verbose_name = "Hisobot"
        verbose_name_plural = "Hisobotlar"
        unique_together = ('name', 'startup')

    @property
    def get_fields(self):
        return self.fields.all()

class RevenueFields(BaseModel):
    name = models.CharField("Hisobot nomi", unique=True, max_length=120)
    value = models.IntegerField("Hisobot qiymati", default=0)

    revenue = models.ForeignKey(Revenues, models.CASCADE, verbose_name="Hisobot",
                                related_name="fields")

    is_plus = models.BooleanField(default=True)
    # checking increase process.
    percentage = models.FloatField("O'zgarish miqdori % da", default=100.0)

    class Meta(BaseModel.Meta):
        abstract = False
        verbose_name = "Hisobot sohasi"
        verbose_name_plural = "Hisobotlar sohasi"
        unique_together = ('name', 'revenue')