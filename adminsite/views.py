from django.shortcuts import render, redirect
from products.models import ProductDetails, Category, VariationColor, VariationSize
from django.contrib import messages

app_name = 'adminsite'


# Create your views here.

def add_product(request):
    cat = Category.objects.all()
    context = {'cat': cat}
    if request.method == "GET":

        return render(request, 'addProduct.html', context)
    elif request.method == "POST":
        category_name = request.POST.get('cat')
        product_name = request.POST['pname']
        image = request.POST['img']
        img = 'pics/' + image
        description = request.POST['description']
        price = request.POST['price']
        discount = request.POST['discount']
        size = request.POST.getlist('size')
        color = request.POST['color']

        get_category_id = Category.objects.get(name=category_name)

        insert = ProductDetails.objects.create(productName=product_name, image=img, description=description,
                                               price=price, discountVal=discount,
                                               categoryKey=get_category_id)
        insert.save()

        get_id = ProductDetails.objects.get(productName=product_name)
        for i in size:
            VariationSize.objects.create(product_id=get_id.id, name=i)
        color_list = color.split(' ')
        for i in color_list:
            VariationColor.objects.create(product_id=get_id.id, name=i)

        return render(request, 'addProduct.html', context)


def get_category(request):
    if request.method == "GET":
        context = {
            'cat': Category.objects.all()
        }
        return render(request, 'getCategory.html', context)


def show_product(request):
    if request.method == "POST":
        get_cat = Category.objects.get(name=request.POST.get('cat'))
        print(get_cat.name)
        print(get_cat.id)
        a = ProductDetails.objects.filter(categoryKey_id=get_cat.id)
        context = {
            'product': a
        }
        return render(request, 'showProductForUpdate.html', context)


def update_product(request, id):
    obj = ProductDetails.objects.get(id=id)
    if request.method == "GET":
        a = ProductDetails.objects.get(id=id)

        context = {
            'product': a
        }
        size = VariationSize.objects.filter(product_id=id)
        color = VariationColor.objects.filter(product_id=id)
        s = ''
        c = ''
        for i in size.iterator():
            s = s + i.name + " "
        for i in color.iterator():
            c = c + i.name + " "
        print(s)
        context = {
            'product': a,
            'color': c,
            'size': s
        }
        return render(request, 'updateProduct.html', context)
    elif request.method == "POST":
        if 'update' in request.POST:
            product_name = request.POST['pname']
            image = request.POST['img']
            img = 'pics/' + image
            description = request.POST['description']
            price = request.POST['price']
            discount = request.POST['discount']
            size = request.POST.getlist('size')
            color = request.POST['color']
            available = request.POST.getlist('avl')

            p_name = ProductDetails.objects.filter(productName=product_name)
            flag = False
            if product_name:
                flag = True
                p_name = ProductDetails.objects.filter(productName=product_name)
                if p_name.exists():
                    pass
                else:
                    obj.productName = product_name
            if image:
                flag = True
                img = 'pics/' + image
                obj.image = image
            if description:
                flag = True
                obj.description = description
            if price:
                flag = True
                obj.price = price
            if discount:
                flag = True
                obj.discount = discount
            if size:
                flag = True
                for i in size:
                    VariationSize.objects.create(product_id=id, name=i)
            if color:
                flag = True
                color_list = color.split(' ')
                for i in color_list:
                    VariationColor.objects.create(product_id=id, name=i)

            if available:
                flag = True
                obj.available = available[0]
            if flag:
                obj.save()
                return redirect('adminsite:get_category')
            else:
                pass


        elif 'delete' in request.POST:
            obj.delete()
            return redirect('adminsite:get_category')