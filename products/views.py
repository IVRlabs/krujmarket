# Стандартные импорты Django
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

# Локальные импорты
from .models import Category, Product

class ProductListView(ListView):
    """
    Список всех активных товаров.
    Использует шаблон 'products/list.html'.
    """
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12  # Пагинация: 12 товаров на странице

    def get_queryset(self):
        """Возвращает только активные товары (is_active=True)."""
        return Product.objects.filter(is_active=True).select_related('category')

class CategoryDetailView(DetailView):
    """
    Детальная страница категории со списком её товаров.
    Использует шаблон 'products/category_detail.html'.
    """
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'  # Параметр из URL

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст список товаров категории.
        """
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            category=self.object,
            is_active=True
        )
        return context

class ProductDetailView(DetailView):
    """
    Детальная страница товара.
    Использует шаблон 'products/detail.html'.
    """
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Только активные товары + оптимизация запросов."""
        return Product.objects.filter(is_active=True).select_related('category')


from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactsView(TemplateView):
    template_name = 'contacts.html'

class BlogView(TemplateView):
    template_name = 'blog.html'


from django.shortcuts import redirect
from cart.models import Cart, CartItem


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    # Логика добавления товара в корзину

    return redirect('product_list')


from django.views.generic import ListView
from django.db.models import Q
from .models import Product
from .forms import ProductFilterForm


class ProductFilterView(ListView):
    """
    Представление для фильтрации товаров с обработкой GET-параметров
    """
    model = Product
    template_name = 'products/product_list.html'  # Используем тот же шаблон
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductFilterForm(self.request.GET)

        if form.is_valid():
            # Фильтрация по категории
            if category := form.cleaned_data['category']:
                queryset = queryset.filter(category=category)

            # Фильтрация по цене
            price_filters = Q()
            if price_min := form.cleaned_data['price_min']:
                price_filters &= Q(price__gte=price_min)
            if price_max := form.cleaned_data['price_max']:
                price_filters &= Q(price__lte=price_max)
            queryset = queryset.filter(price_filters)

            # Сортировка
            if sort_by := form.cleaned_data['sort']:
                if sort_by == 'price_asc':
                    queryset = queryset.order_by('price')
                elif sort_by == 'price_desc':
                    queryset = queryset.order_by('-price')
                elif sort_by == 'newest':
                    queryset = queryset.order_by('-created_at')

        return queryset.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET)
        context['is_filtered'] = bool(self.request.GET)
        return context


