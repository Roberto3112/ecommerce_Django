from django.db import models

# We'll use the default model for user that Django have.
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    # if our product is digital don't need to be shipped, else if is fisical 
    # need to be shipped. True for digital, False for fisical.
    digital = models.BooleanField(default=False, blank=False)
    # For image we've to install python pillow
    # Python Pillow: is a image procesor library that allow add image to the model. 
    # Once we add this, we have to add media_ROOT in settings.py to say where the images will be store.
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    # This function is for if our product don't have an images dont throw an error.
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)  
    # if is False: Means the cart isn't close, the customer keep picking products.
    # if is True: Means the cart is closed, the custormer isn't picking more products.
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def get_cart_total(self):
        # We get ours order items.
        orderitem = self.orderitem_set.all()

        # we do a loop for get all our prices.
        total = sum([item.get_total for item in orderitem])
        return total

    @property
    def get_total_item(self):
        # We get ours order items.
        orderitem = self.orderitem_set.all()

        # we do a loop for get all our items.
        total = sum([item.quantity for item in orderitem])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product}, quantity: {self.quantity}"
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        
        return total

class shippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
