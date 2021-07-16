from django.contrib import admin
from order.models import Order, Cart
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)