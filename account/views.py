import account
from django.shortcuts import render, redirect
from django.http import HttpResponse
from account.forms import RegistrationFrom
from django.contrib.auth.models import User
from account.models import Profile
from account.forms import RegistrationFrom, ProfileForm
from django.db.models import Subquery
from  order.models import Order
from django.contrib.auth.models import User, auth
from django.contrib import messages
from account.models import Profile
from order.models import Order , Cart
from django.db.models import Count
from django.shortcuts import get_list_or_404, get_object_or_404


# Create your views here.
app_name = 'account'


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                return redirect('adminsite:adminOptions')
            else:
                return redirect("/")

    else:
         return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def registration(request):
    if request.method == "POST":
        fullname = request.POST['name']
        username = request.POST['uname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        address = request.POST['address']
        phone = request.POST['phone']

        if password1 == password2:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                print("user name")

            else:
                user = User.objects.create_user(username=username, email=email, password=password2)
                user.save()
                p = User.objects.get(username=username)
                Profile.objects.filter(user_id=p.id).update(full_name=fullname, address=address, phone=phone)
                return redirect('account:login')
        else:
            print("not match")

    return render(request, 'registration.html')


def userProfile(request):
    count_pending_order = Order.objects.filter(user=request.user, delivered = False).count()
    count_total_order = Order.objects.filter(user=request.user).count()
    context = {
        'pending' : count_pending_order,
        'total' : count_total_order
    }
    
    return render(request, 'userProfile.html',context)


def order_details_for_user(request):
    order_query = Order.objects.filter(user=request.user).order_by('delivered')
    if order_query.exists():
        
        if request.method == 'GET':
            order_query.reverse()
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
        return HttpResponse("No order available")



def details_order_show(request, id):
    hold_order = get_object_or_404(Order, id = id)
    user_info = get_object_or_404(Profile, user_id = request.user)
    context = {
        'orderInfo' : hold_order,
        'userInfo' : user_info,
    
    }
    return render(request, 'userOrderDetailsShow.html', context)


