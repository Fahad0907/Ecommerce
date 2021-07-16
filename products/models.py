from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductDetails(models.Model):
    productName = models.CharField(max_length=50)
    image = models.ImageField(upload_to='pics')
    description = models.TextField()
    price = models.IntegerField()
    discountVal = models.IntegerField()
    available = models.BooleanField(default=True)
    categoryKey = models.ForeignKey(Category, on_delete=models.CASCADE)

    def return_id(self):
        a = ProductDetails.objects.get(productName=self.productName)

    def __str__(self):
        return self.productName


class ProductImages(models.Model):
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pics')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.productName


class VariationColor(models.Model):
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class VariationSize(models.Model):
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
