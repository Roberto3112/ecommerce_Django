from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from collections import Counter
import json
import datetime

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
    context = {'products':products, 'items':items, 'order':order, 'cartItems':cartItems , 'shipping': False}
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
        cartItems = order['get_cart_item']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_item
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_item':0, 'shipping': False}
        cartItems = order['get_cart_item']
    context = {'items':items,'order':order, 'cartItems':cartItems}
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

def processOrder(request):
        data = json.loads(request.body)
        shippingInfo = data['shipping']    
        
        # Here we're reciving the form dictionary and accesing to the total value.
        total = float(data['form']['total'])

        # This to add time of the order in our model.
        transaction_id = datetime.datetime.now().timestamp()

        if request.user.is_authenticated:
            customer = request.user.customer
            order, create = Order.objects.get_or_create(customer=customer, complete=False)
            order.transaction_id = transaction_id    

            if total == float(order.get_cart_total):
                order.complete = True
            order.save()

            if order.shipping == True:
                shippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode =  data['shipping']['zipcode'],
                date_added = transaction_id
                )
                
        else:
            print('User is not logged in')
        return JsonResponse("We're sending the form",safe=False)