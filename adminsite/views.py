from account.models import Profile
from django.http.response import HttpResponse
from order.models import Order
from django.shortcuts import render, redirect
from products.models import ProductDetails, Category, VariationColor, VariationSize
from django.contrib import messages
from Coupon.models import Coupon
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import user_passes_test



app_name = 'adminsite'


# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def get_category(request):
    if request.method == "GET":
        context = {
            'cat': Category.objects.all()
        }
        return render(request, 'getCategory.html', context)

@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def add_coupon(request):
    if request.method == 'GET':
        return render(request, 'Coupon.html')
    elif request.method == 'POST':
        code = request.POST['fname']
        start_time = request.POST['startTime']
        end_time = request.POST['endTime']
        discount = request.POST['discount']
        active = request.POST.getlist('active')
        activeStatus = False
        if active:
            activeStatus = True
        check_code = Coupon.objects.filter(code=code)
        if check_code.exists():
            messages.warning(request,'Coupon already exists')
            return redirect('adminsite:addCoupon')
        else:
            Coupon.objects.create(code=code, startTime= start_time,endTime = end_time,discount=discount ,active=activeStatus)
            return redirect('adminsite:adminOptions')

@user_passes_test(lambda u: u.is_superuser)
def admin_options(request):
    return render(request, 'adminOptions.html')


@user_passes_test(lambda u: u.is_superuser)
def get_coupon(request):
    if request.method == 'POST':
        print(request.POST.get('coupon'))
        getCup = Coupon.objects.get(code=request.POST.get('coupon'))
        context = {
            'coupon' : getCup
        }
        return render(request, 'updateCoupon.html', context)

    elif request.method == 'GET':
        query = Coupon.objects.all()
        context = {
            'query' : query
        }
        return render(request, 'getCoupon.html', context)

@user_passes_test(lambda u: u.is_superuser)
def show_all_order(request):
    
    order_query = Order.objects.all().order_by('delivered')
    
    if order_query.exists():
        if request.method == 'GET':
            context = {
                'order_query' : order_query
            }
        if request.method == 'POST':
            hold_order = request.POST['searchOrder']
            print(hold_order)
            get_order = Order.objects.filter(orderId = hold_order)
            if get_order.exists():
                context = {
                    'order_query' : get_order
                }
            else:
                context={}
                messages.info(request, 'Invalid order id')
            

        return render(request, 'allOrder.html', context)
    else:
        order_query = Order.objects.all().order_by('crated')
        context = {
                    'order_query' : order_query
        }
        return render(request, 'allOrder.html', context)


@user_passes_test(lambda u: u.is_superuser)
def order_details(request, id):
    if request.method == 'POST':
        hold_order = get_object_or_404(Order, id = id)
        hold_order.delivered = True
        hold_order.save()
        return redirect('adminsite:allOrder')
    hold_order = get_object_or_404(Order, id = id)
    user_info = get_object_or_404(Profile, user_id = hold_order.user)
    context = {
        'orderInfo' : hold_order,
        'userInfo' : user_info,
    
    }
    return render(request, 'orderDetails.html', context)

