from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/increase/<int:pk>/', views.cart_increase, name='cart_increase'),
    path('cart/decrease/<int:pk>/', views.cart_decrease, name='cart_decrease'),
]