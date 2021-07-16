from django.shortcuts import render, redirect
from django.http import HttpResponse
from account.forms import RegistrationFrom
from django.contrib.auth.models import User
from account.models import Profile
from account.forms import RegistrationFrom, ProfileForm
from django.db.models import Subquery
from  order.models import Order

# Create your views here.
app_name = 'account'


def login(request):
    if request.user.is_authenticated:
        return HttpResponse('you are authinticated')
    else:
        form = RegistrationFrom()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


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


def show_order(request):
    order = Order.objects.filter(ordered=False)
    context = {}
    context['order'] = order
    return render(request, 'userOrder.html', context)

