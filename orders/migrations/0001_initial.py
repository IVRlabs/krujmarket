# Generated by Django 5.0 on 2025-05-19 00:19

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True, verbose_name='Ключ сессии')),
                ('payment_type', models.CharField(choices=[('full', 'Полная оплата'), ('prepay', 'Предоплата 30%'), ('installment', 'Рассрочка')], default='full', max_length=20, verbose_name='Тип оплаты')),
                ('total', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Общая сумма')),
                ('prepayment', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Предоплата')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('prepaid', 'Ожидает оплаты'), ('paid', 'Оплачен'), ('completed', 'Завершен'), ('canceled', 'Отменен')], default='new', max_length=20, verbose_name='Статус')),
                ('items', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, verbose_name='Товары')),
                ('customer_name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created_at'],
            },
        ),
    ]
