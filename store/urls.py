from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    # path('cart/edit_cart',views.editCart,name='editCart'),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/',views.updateItem,name='updateItem'),
]