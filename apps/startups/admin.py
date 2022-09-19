from django.contrib import admin

# Register your models here.
from .models import Startups, Revenues, RevenueFields


@admin.register(Startups)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')



@admin.register(Revenues)
class RevenuesAdmin(admin.ModelAdmin):
    list_display = ('name', 'startup', 'created_by')


@admin.register(RevenueFields)
class RevenueFieldsAdmin(admin.ModelAdmin):
    list_display = ('name', 'revenue', 'created_by')