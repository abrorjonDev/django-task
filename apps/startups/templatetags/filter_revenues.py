from django import template

from ..models import Startups, Revenues, Outgoings
from apps.user.models import User


register = template.Library()

@register.filter(name="filter_revenues")
def filter_revenues(value: Startups, user: User):
    return Revenues.objects.filter(startup=value, author=user).first()
