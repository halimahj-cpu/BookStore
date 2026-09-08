from django.contrib import admin
from .models import Book, CartItem, Wishlist, Order

admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(Order)