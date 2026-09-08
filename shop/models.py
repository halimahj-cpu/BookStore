from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=200, verbose_name="Автор")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='books/', verbose_name="Обложка", blank=True, null=True)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField(max_length=150, verbose_name="Имя получателя")
    address = models.TextField(verbose_name="Адрес доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    def __str__(self):
        return f"Заказ №{self.id} от {self.full_name}"