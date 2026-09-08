from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from .forms import OrderForm, RegisterForm
from .models import Book, CartItem, Wishlist
from django.contrib.auth import logout


def index(request):
  genre_query = request.GET.get('genre', '')
  books = Book.objects.all()

  if genre_query:
    books = books.filter(genre__icontains=genre_query)

  paginator = Paginator(books, 6)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(
      request,
      'shop/index.html',
      {'page_obj': page_obj, 'selected_genre': genre_query},
  )


def book_detail(request, pk):
  book = get_object_or_404(Book, pk=pk)
  return render(request, 'shop/book_detail.html', {'book': book})


def cart_detail(request):
  if not request.user.is_authenticated:
    return redirect('login')
  items = CartItem.objects.filter(user=request.user)
  total = sum(item.book.price * item.quantity for item in items)
  return render(request, 'shop/cart.html', {'items': items, 'total': total})


def cart_add(request, pk):
  if not request.user.is_authenticated:
    return redirect('login')
  book = get_object_or_404(Book, pk=pk)
  cart_item, created = CartItem.objects.get_or_create(
      user=request.user, book=book
  )
  if not created:
    cart_item.quantity += 1
    cart_item.save()

  # Возвращаем пользователя на ту страницу, с которой он нажал кнопку
  return redirect(request.META.get('HTTP_REFERER', 'index'))


def cart_remove(request, pk):
  item = get_object_or_404(CartItem, pk=pk, user=request.user)
  item.delete()
  return redirect('cart_detail')


def wishlist_view(request):
  if not request.user.is_authenticated:
    return redirect('login')
  wishlist = Wishlist.objects.filter(user=request.user)
  return render(request, 'shop/wishlist.html', {'wishlist': wishlist})


def toggle_wishlist(request, pk):
  if not request.user.is_authenticated:
    return redirect('login')
  book = get_object_or_404(Book, pk=pk)
  item = Wishlist.objects.filter(user=request.user, book=book)
  if item.exists():
    item.delete()
  else:
    Wishlist.objects.create(user=request.user, book=book)
  return redirect('index')


def checkout(request):
  if not request.user.is_authenticated:
    return redirect('login')
  items = CartItem.objects.filter(user=request.user)
  if not items.exists():
    return redirect('index')

  total = sum(item.book.price * item.quantity for item in items)

  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      order = form.save(commit=False)
      order.user = request.user
      order.total_price = total
      order.save()
      items.delete()
      return render(request, 'shop/order_success.html', {'order': order})
  else:
    form = OrderForm()

  return render(
      request, 'shop/checkout.html', {'form': form, 'total': total, 'items': items}
  )


def register_view(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
  else:
    form = RegisterForm()
  return render(request, 'shop/register.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('index')
  else:
    form = AuthenticationForm()
  return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
  logout(request)
  return redirect('index')

def cart_increase(request, pk):
  if not request.user.is_authenticated:
    return redirect('login')
  item = get_object_or_404(CartItem, pk=pk, user=request.user)
  item.quantity += 1
  item.save()
  return redirect('cart_detail')


def cart_decrease(request, pk):
  if not request.user.is_authenticated:
    return redirect('login')
  item = get_object_or_404(CartItem, pk=pk, user=request.user)
  if item.quantity > 1:
    item.quantity -= 1
    item.save()
  else:
    item.delete()  # Если количество стало 0, удаляем товар из корзины
  return redirect('cart_detail')