from django import forms
from .models import Category

class ProductFilterForm(forms.Form):
    """
    Форма фильтрации товаров с базовыми полями:
    - Выбор категории
    - Диапазон цен
    - Сортировка
    """
    SORT_CHOICES = [
        ('price_asc', 'От дешевых'),
        ('price_desc', 'От дорогих'),
        ('newest', 'Новинки'),
    ]

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Категория",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    price_min = forms.IntegerField(
        required=False,
        label="Цена от",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '₽',
            'min': 0
        })
    )

    price_max = forms.IntegerField(
        required=False,
        label="Цена до",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '₽',
            'min': 0
        })
    )

    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="Сортировка",
        widget=forms.Select(attrs={'class': 'form-select'})
    )