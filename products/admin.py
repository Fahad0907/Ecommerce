from django.contrib import admin
from .models import Category, ProductDetails, ProductImages, VariationColor, VariationSize


# Register your models here.


admin.site.register(ProductImages)
admin.site.register(Category)
admin.site.register(ProductDetails)
admin.site.register(VariationColor)
admin.site.register(VariationSize)