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

