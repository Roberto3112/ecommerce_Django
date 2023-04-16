from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from collections import Counter
import json

# Create your views here.
def store(request):

       # We will see if our user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer

        # Here, we'll create an order or get if already exist.  
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # This is for make a query of the child object, with this we will get all our orders 
        # First we put the parent object and after the child object uppercase + _set.all()
        # to get all the child objects.
        items = order.orderitem_set.all()
        cartItems = order.get_total_item

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all() 
    context = {'products':products, 'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    # We will see if our user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer

        # Here, we'll create an order or get if already exist.  
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # This is for make a query of the child object, with this we will get all our orders 
        # First we put the parent object and after the child object uppercase + _set.all()
        # to get all the child objects.
        items = order.orderitem_set.all()
        cartItems = order.get_total_item
        
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0}
        cartItems = order['get_total_item']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    # this for hide or show the shipping form if our product is digital or not.
        digital = ''
        for item in items: 
            if item.product.digital == False:
                digital = 'False'
                break
            else:
                digital = 'True'

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0}
        digital = ''

    context = {'items':items,'order':order, 'digital':digital}
    return render(request, 'store/checkout.html', context)

def updateItem(request):

    # This for access to the data that we sent from js to update_item.
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('Action:', action)
    print('ProductID:', productID)

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    product = Product.objects.get(id=productID)
    orderItem,created = OrderItem.objects.get_or_create(product=product, order=order)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# def editCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    orderItem = OrderItem.objects.get(id=productId)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse("We're editing the cart...", safe=False)