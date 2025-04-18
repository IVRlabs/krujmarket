from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product, Category
from .forms import ProductFilterForm

from django.db.models import Count
from .models import Category


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        # Фильтрация по категории
        if category_slug := self.request.GET.get('category'):
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)
        return context

class ProductDetailView(DetailView):
    """
    Детальная страница товара.
    Показывает полную информацию о конкретном товаре.
    """
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Только активные товары + оптимизация запросов к БД"""
        return Product.objects.filter(is_active=True).select_related('category')

class ProductFilterView(ListView):
    """
    Список товаров с фильтрацией по:
    - категории
    - цене (диапазон)
    - сортировке
    Наследует базовые параметры от ProductListView.
    """
    model = Product
    template_name = 'products/list.html'  # Используем тот же шаблон
    context_object_name = 'products'
    paginate_by = 12
    form_class = ProductFilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('category'):
            queryset = queryset.filter(
                category__slug=self.request.GET['category']
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET)
        return context