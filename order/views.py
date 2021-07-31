from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from products.models import ProductDetails
from order.models import Order, Cart
from django.utils import timezone
from Coupon.models import Coupon
from account.models import Profile
app_name = 'order'


# Create your views here.
def addtocart(request, id):
    if request.method == 'POST':
        size = request.POST.get('size')
        color = request.POST.get('color')
        qty = int(request.POST['qty'])
        
        item = ProductDetails.objects.get(id=id)
        check_item_in_cart = Cart.objects.get_or_create(item=item, user=request.user, purchased=False
                                                        , size=size, color=color)

        check_order = Order.objects.filter(user=request.user, ordered=False)
        if check_order.exists():

            check_order = check_order[0]

            if check_order.orderItems.filter(item=item).exists():
                check_item_in_cart[0].quantity += qty
                check_item_in_cart[0].save()
                check_order.orderItems.add(check_item_in_cart[0])

            else:
                check_order.orderItems.add(check_item_in_cart[0])

        else:
      
            check_item_in_cart[0].quantity = qty
            check_item_in_cart[0].save()
            order = Order.objects.create(user=request.user)
            order.save()
            order.orderItems.add(check_item_in_cart[0])

    return redirect('homepage')


    

def showcart(request):
    #print(request.user.id)
    cart = Cart.objects.filter(user=request.user, purchased=False)
    order = Order.objects.filter(user=request.user, ordered=False)
    a = 0.0
    if cart.exists() and order.exists():
        order = order[0]
        print(order.get_total_price())
        if request.method == "POST":
            if 'checkout' in request.POST:
                cash_on_delivery = request.POST.get('cashOnDelivery')
                online_payment = request.POST.get('onlinePayment')
                if cash_on_delivery:
                    query = Profile.objects.get(user_id = request.user.id)
                    order.orderId = 'zAq' + str(order.id) + 'tsw'
                    order.paymentType = cash_on_delivery
                    order.couponCode = request.session.get('couponCode')
                    print(request.session.get('couponCode'))
                    order.discount =  request.session.get('discount')
                    if request.session.get('ammount'):
                        order.amount = request.session.get('ammount')
                    else:
                        order.amount = order.get_total_price()
                    order.ordered = True
                    order.save()
                    cart.update(purchased=True)
                    return redirect('account:userProfile')
                    
                elif online_payment:
                    pass
            elif 'coupon' in request.POST:
                coupon_code = request.POST['couponCode']
                check_coupon = Coupon.objects.get(code = coupon_code)
                if coupon_code:
                    current_time = timezone.now()
                    if check_coupon.endTime >= current_time and check_coupon.active:
                        a = (float(check_coupon.discount) * order.get_total_price()) / 100
                        request.session['couponCode'] = coupon_code
                        request.session['discount'] = check_coupon.discount
                        request.session['ammount'] = order.get_total_price() - a
                        
              
                

          
        total_after_using_coupon = order.get_total_price() - a
        context = {
            'cart': cart,
            'order': order,
            'addCoupon' : total_after_using_coupon
        }
        return render(request, 'showcart.html', context)
    else:
        return HttpResponse('No product in your cart')  


def update_add_single_element(request, id):
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        check_cart = Cart.objects.get(id=id, purchased=False)
        check_cart.quantity += 1
        check_cart.save()
        order.orderItems.remove(check_cart)
        order.orderItems.add(check_cart)
        return redirect('showcart')


def update_delete_single_element(request, id):
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        check_cart = Cart.objects.get(id=id, purchased=False)

        if check_cart.quantity == 0:
            order.orderItems.remove(check_cart)
            check_cart.delete()
            return redirect('showcart')
        else:
            check_cart.quantity -= 1
            check_cart.save()
            order.orderItems.remove(check_cart)
            order.orderItems.add(check_cart)
            return redirect('showcart')


def delete_from_cart(request, id):
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        check_cart = Cart.objects.get(id=id, purchased=False)
        order.orderItems.remove(check_cart)
        check_cart.delete()
        return redirect('showcart')
