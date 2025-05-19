from django.db import models
from django.conf import settings
from products.models import Product  # Импорт модели товара из приложения market
from django.db.models import Sum, F
import json

class CartManager(models.Manager):
    def get_for_request(self, request):
        """Получает корзину для текущего запроса"""
        if request.user.is_authenticated:
            return self.get(user=request.user)
        else:
            return self.get(session_key=request.session.session_key)




class Cart(models.Model):
    """
    Модель корзины пользователя.
    Хранит связь с пользователем (для авторизованных) или session_key (для гостей)
    """
    objects = CartManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Ключ сессии"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def get_items_json(self):
        return json.dumps([
            {
                'name': item.product.name,
                'price': float(item.price),
                'quantity': item.quantity
            }
            for item in self.items.all()
        ])

    def has_in_stock_items(self):
        return self.items.filter(product__in_stock=True).exists()

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        unique_together = [['user', 'session_key']]  # Предотвращаем дубликаты

    def __str__(self):
        return f"Корзина {self.user or self.session_key}"

    @property
    def total_quantity(self):
        return self.items.aggregate(
            total=Sum('quantity')
        )['total'] or 0

    @property
    def total_price(self):
        return self.items.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0

class CartItem(models.Model):
    """
    Элемент корзины. Связывает товар с корзиной, хранит количество и цену
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за единицу"
    )

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = [['cart', 'product']]  # Один товар - одна позиция

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.price * self.quantity