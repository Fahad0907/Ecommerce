from django.shortcuts import render, get_object_or_404, redirect
from products.models import ProductDetails
from order.models import Order, Cart

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
    cart = Cart.objects.filter(user=request.user, purchased=False)
    order = Order.objects.filter(user=request.user, ordered=False)

    if cart.exists() and order.exists():
        order = order[0]
        print(order.get_total_price())
        context = {
            'cart': cart,
            'order': order
        }
        return render(request, 'showcart.html', context)


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
