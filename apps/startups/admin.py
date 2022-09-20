from django.contrib import admin

from .models import Outgoings, Startups, Revenues

# Register your models here.


admin.site.register(Startups)
admin.site.register(Outgoings)
@admin.register(Revenues)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ("id", "startup", "author")
