from products.models import Category
from django import template
register = template.Library()

@register.filter
def category(user):
    return Category.objects.all()