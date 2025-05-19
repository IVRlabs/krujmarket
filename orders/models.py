from django.db import models
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json


class Order(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('full', 'Полная оплата'),
        ('prepay', 'Предоплата 30%'),
        ('installment', 'Рассрочка')
    ]

    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('prepaid', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен')
    ]

    # Связи
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    session_key = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='Ключ сессии'
    )

    # Платежи
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        default='full',
        verbose_name='Тип оплаты'
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Общая сумма'
    )
    prepayment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Предоплата'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    # Товары
    items = models.JSONField(
        encoder=DjangoJSONEncoder,
        verbose_name='Товары'
    )

    # Клиентские данные
    customer_name = models.CharField(
        max_length=100,
        verbose_name='ФИО'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )

    # Даты
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} ({self.get_status_display()})"

    @property
    def items_list(self):
        """Возвращает товары в виде списка"""
        try:
            return json.loads(self.items)
        except:
            return []

    def save(self, *args, **kwargs):
        """Автоматический расчет предоплаты"""
        if self.payment_type == 'prepay' and not self.prepayment:
            self.prepayment = self.total * 0.3
        super().save(*args, **kwargs)