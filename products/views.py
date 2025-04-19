from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import Product, Category
from .forms import ProductFilterForm


class ProductListView(ListView):
    """
    Список товаров с базовой фильтрацией по категориям.
    Оптимизирован для работы с вашей структурой моделей.
    """
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12  # Добавляем пагинацию

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        # Оптимизация запросов
        queryset = queryset.select_related('category').prefetch_related('additional_images')

        # Фильтрация по категории
        if category_slug := self.request.GET.get('category'):
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Аннотируем категории количеством товаров
        context['categories'] = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).filter(product_count__gt=0)

        # Добавляем форму фильтрации
        context['filter_form'] = ProductFilterForm(self.request.GET)

        return context


class ProductDetailView(DetailView):
    """
    Детальная страница товара с галереей изображений.
    Полностью соответствует вашей модели Product.
    """
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """Оптимизированный запрос с подгрузкой всех связанных данных"""
        return Product.objects.filter(is_active=True).select_related(
            'category'
        ).prefetch_related(
            'additional_images'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Формируем список всех изображений (основное + дополнительные)
        context['all_images'] = [product.main_image] + [
            img.image for img in product.additional_images.all()
        ]

        # Мета-данные для SEO
        context['meta'] = product.as_meta(self.request)

        return context


class ProductFilterView(ProductListView):
    """
    Расширенная версия ProductListView с дополнительными фильтрами.
    Наследует все базовые функции.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductFilterForm(self.request.GET)

        if form.is_valid():
            # Фильтрация по цене
            if price_min := form.cleaned_data.get('price_min'):
                queryset = queryset.filter(price__gte=price_min)

            if price_max := form.cleaned_data.get('price_max'):
                queryset = queryset.filter(price__lte=price_max)

            # Сортировка
            if sort_by := form.cleaned_data.get('sort_by'):
                if sort_by == 'price_asc':
                    queryset = queryset.order_by('price')
                elif sort_by == 'price_desc':
                    queryset = queryset.order_by('-price')
                elif sort_by == 'newest':
                    queryset = queryset.order_by('-created_at')

        return queryset