from django.db import models
from django.contrib.auth.models import User
from products.models import ProductDetails

app_name = 'order'


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    purchased = models.BooleanField(default=False)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} X {self.item}"

    def get_total(self):
        total = self.item.price * self.quantity
        total = format(total, '0.2f')
        return total


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderItems = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    crated = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=150, blank=True, null=True)
    orderId = models.CharField(max_length=150, blank=True, null=True)

    def get_total_price(self):
        total = 0
        for i in self.orderItems.all():
            total = total + float(i.get_total())
        return total

