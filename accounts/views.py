from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Customer, Products, Order
from .form import OrderForm, CreateUserForm

from .filters import OrderFilter
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    pending = Order.objects.filter(status="Pending").count()
    delivered = Order.objects.filter(status="Delivered").count()
    # creating pagination
    p = Paginator(orders, 5)
    # getting number of pages
    page_num = request.GET.get('page', 1)
    try:
        orders = p.page(page_num)
    except EmptyPage:
        orders = p.page(1)
    context = {
        'customers': customers, 'orders': orders, 
        'total_customers': total_customers, 
        'total_orders': total_orders, 'pending': pending,
        'delivered': delivered
    }
    return render(request, 'accounts/dashboard.html', context)

def loginPage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid Username OR Password")
    return render(request, "accounts/login.html")

def logoutUser(request):
    logout(request)
    return redirect('account:login')

def register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data.get('username') 
            # if User.objects.filter(email=email).exists():
            #     messages.info(request, "Email in used")
            #     return redirect('accounts:register')
            # else:
            form.save()
            # user = form.cleaned_data.get('username')
            # print(form.cleaned_data.get('username'))
            messages.success(request, username + ' Registered successfully ')
            return redirect('accounts:login')
    context = {
        'form': form
    }
    return render(request, "accounts/register.html", context)

@login_required(login_url='login')
def products(request):
    products = Products.objects.all()
    context = {
        'products':products
    }
    return render(request, "accounts/products.html", context )

@login_required(login_url='login')
def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.order_set.all()
    orders_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customers':customers, 'orders':orders, 'orders_count':orders_count, 'myFilter':myFilter
    }
    return render(request, "accounts/customer.html", context)

@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, "accounts/order_form.html", context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method=="POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, "accounts/order_form.html", context )

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect('/')