from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import *
import json


# Create your views here.
def index(request):
    categories=Category.objects.all()
    s=request.GET.get('s') if request.GET.get('s') != None else ''
    order=''
    if request.user.is_authenticated:
        user=request.user.id
        try:
            order=Order.get_panding_by_customer_id(user)
        except:
            order=''
    products=Products.objects.filter(
            Q(category_name__name__contains=s) |
            Q(name__contains=s) |
            Q(price__contains=s)
    )
    return render(request,'pages/index.html',{'products':products,'categories':categories,'order':order})

def product_view(request,pk):
    product=Products.objects.get(id=pk)
    categories=Category.objects.all()
    if request.user.is_authenticated:
        user=request.user.id
        try:
            order=Order.get_panding_by_customer_id(user)
        except:
            order=''

    return render(request,'pages/product.html',{'product':product,'categories':categories,'order':order})

def cart(request):
    context={}
    if request.user.is_authenticated:
        user=request.user.id
        try:
            order=Order.get_panding_by_customer_id(user)
            items=order.orderitem_set.all()

            context['order']=order
            context['items']=items
        except:
            context['order']=''
            context['items']=''
        context['user']=user
        return render(request,'pages/cart.html',context)

    return render(request,'pages/cart.html')
    
def checkout(request):
    context={'order':'','items':''}
    if request.method == "POST":

        if request.user.is_authenticated:
                user=request.user.id
                try:
                    all_items=[]
                    order=Order.get_panding_by_customer_id(user)
                    items=order.orderitem_set.all()

                    context['order']=order
                    context['items']=items
                except:
                    context['order']=''
                    context['items']=''
                context['user']=user
                return render(request,'pages/checkout.html',context)
    return redirect('cart')

def profile(request):
    context={}
    if request.user.is_authenticated:
        try:
            order=Order.get_panding_by_customer_id(request.user.id)
            context['order']=order
        except:
            context['order']=''

        try:
            customer=Customer.objects.get(user__id=request.user.id)
            context['customer']=customer
            # print(customer)
        except:
            messages.warning(request,'you are login with wrong account !!!')
            return redirect('index')
            pass

    return render(request,'pages/profile.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    orderId=data['orderId']

    product=Products.get_product_by_id(productId)
    order=Order.objects.get(id=orderId)
    orderItem=OrderItem.objects.get(order=order,product=product)

    if action == 'add':
        orderItem.quantity+=1
    elif action == 'remove':
        orderItem.quantity-=1


    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    if action == 'add':
        return JsonResponse('add',safe=False)
    elif action == 'remove':
        return JsonResponse('remove',safe=False)

    return JsonResponse('working',safe=False)


def addCart(request,pk):
    if request.user.is_authenticated:
        try:
            if OrderItem.add_product_by_id(request,pk,request.user.id):
                return redirect('cart')
            else:
                messages.success(request,'Product added Successfully')
        except:
            messages.warning(request,'you are login with wrong account !!!')
            pass
    else:
        messages.error(request,'You have to Sign in first to add product in your cart.')
    return redirect('index')

def signInPage(request):

    if request.method == "POST":
        post=request.POST
        try:
            customer=Customer.objects.get(user__username=post.get('username'))
            if customer.user.check_password(post.get('password')):
                login(request,customer.user)
                messages.success(request,f'{customer.user.first_name} you are signed in Successfully....')
                return redirect('index')
            else:
                messages.warning(request,'Password is incorrect')
        except:
            messages.info(request,'You need to register because you are not our customer yet.')
            return redirect('signup')
        

    return render(request,'pages/signin.html')

def signUpPage(request):
    if request.method == "POST":
        post=request.POST
        
        if post.get('password') == post.get('confirm_password'):
            user=User.objects.create_user(username=post.get('username'),password=post.get('password'),first_name=post.get('first_name'),last_name=post.get('last_name'))
            user.save()
            Customer.objects.create(
                user=user,
                name=post.get('first_name') + post.get('last_name')
            )
            messages.success(request,'Sign Up Successfull...')
            return redirect('signin')
        else:
            messages.warning(request,'Password is not match.')

    return render(request,'pages/signup.html')

def logoutUser(request):
    customer=Customer.objects.get(user__id=request.user.id)
    messages.info(request,'You are Sign Out')
    logout(request)
    return redirect('index')

def contact(request):
    try:
        order=Order.get_panding_by_customer_id(request.user.id)
    except:
        order=''
    return render(request,'pages/contact.html',{'order':order})

def orders(request):
    context={}
    if request.user.is_authenticated:
        user=request.user.id
        try:
            all_items=[]
            orders=Order.get_all_by_customer_id(user)
            for order in orders:
                items=order.orderitem_set.all()
                all_items.append(items)

            all_items.reverse()
            context['all_items']=all_items
            print(all_items)
            print()
            print()
            try:
                Order.objects.get(customer__user__id=user,complete=False)
                context['order']=Order.objects.get(customer__user__id=user,complete=False)
            except:
                context['order']=''

        except:
            context['order']=''
            context['items']=''
            context['all_items']=''
        context['user']=user
        return render(request,'pages/order.html',context)

    return render(request,'pages/order.html')

def placeOrder(request,pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            post=request.POST
            try:
                order=Order.objects.get(id=pk,customer__user__id=request.user.id)
                customer=Customer.objects.get(user__id=request.user.id)
                shippingAdd=shippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=post.get('address'),
                    city=post.get('city'),
                    country=post.get('country'),
                    pincode=post.get('pincode')
                )
                order.complete=True
                order.save()
                # shippingAdd.order.complete=True
                messages.success(request,'Your Order is Placed Successfully...')
                return redirect('index')
            except:
                pass
        return redirect('checkout')
    messages.success(request,'You have to login to place an order.')
    return redirect('index')

def addProduct(reqeust):
    categories=Category.objects.all()
    if reqeust.method =="POST":
        post=reqeust.POST
        category=Category.objects.get(name=post.get('category_name'))
        Products.objects.create(
            category_name=category,
            name=post.get('name'),
            description=post.get('description'),
            price=post.get('price'))
        messages.success(reqeust,'Product added successfully...')
        return redirect('index')

    return render(reqeust,'pages/addProduct.html',{'categories':categories})

    
