from django.shortcuts import render
from .models import ProductDetails, Category, ProductImages, VariationSize, VariationColor

app_name = 'product'


# Create your views here.
def homePage(request):
    
    return render(request, "home.html" )


def showProduct(request, id):
    context = {'product': ProductDetails.objects.filter(categoryKey=id)}
    return render(request, "showProduct.html", context)


def productDetails(request, id):
    context = {'size': VariationSize.objects.filter(product_id=id),
               'color': VariationColor.objects.filter(product_id=id), 'product': ProductDetails.objects.get(id=id),
               'Category': Category.objects.all()}
    return render(request, "productDetails.html", context)
