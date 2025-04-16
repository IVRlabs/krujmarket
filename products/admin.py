# Стандартные импорты Django
from autoslug.utils import slugify
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Локальные импорты (модели текущего приложения)
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели Category.
    Позволяет управлять категориями товаров.
    """
    list_display = ('name', 'slug', 'description')  # Поля в списке объектов
    search_fields = ('name',)  # Поля для поиска
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug из name
    ordering = ('name',)  # Сортировка по умолчанию


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

    # Убираем prepopulated_fields для AutoSlugField
    # prepopulated_fields = {'slug': ('name',)}  # Закомментировать или удалить

    date_hierarchy = 'created_at'
    readonly_fields = ('slug',)  # Делаем slug только для чтения

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'price', 'is_active')
        }),
        ('Описание и изображение', {
            'fields': ('description', 'image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Автоматическое сохранение slug, если он пустой"""
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)



