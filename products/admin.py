from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, ProductImage
from django.utils.text import slugify


class ProductImageInline(admin.TabularInline):
    """Инлайн для добавления дополнительных изображений товара"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')
    ordering = ('order',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение
    fields = ('name', 'slug', 'description')           # slug НЕ включаем!
    list_display = ('name', 'slug')            # Для отображения в списке

    # Важно! Метод для обработки slug при сохранении
    def save_model(self, request, obj, form, change):
        if not obj.slug:  # Если slug пустой
            obj.slug = slugify(obj.name)  # Генерируем вручную
        super().save_model(request, obj, form, change)



    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = _('Количество товаров')




    product_count.short_description = _('Количество товаров')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Администрирование товаров с поддержкой галереи изображений"""
    list_display = ('name', 'price', 'category', 'is_active', 'is_featured',
                    'available', 'is_custom', 'created_at', 'main_image_preview')  # Добавили новые поля
    list_filter = ('category', 'is_active', 'is_featured', 'available', 'is_custom')  # Добавили фильтры
    list_editable = ('available', 'is_custom', 'is_active', 'is_featured')  # Быстрое редактирование

    # Остальные настройки остаются без изменений
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('slug', 'created_at', 'main_image_preview')
    inlines = [ProductImageInline]

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'slug', 'category', 'price',
                       ('is_active', 'is_featured', 'available', 'is_custom'))  # Группировка булевых полей
        }),
        (_('Контент'), {
            'fields': ('description', 'main_image', 'main_image_preview')
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        (_('Даты'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    # Существующие методы остаются без изменений
    def main_image_preview(self, obj):
        if obj.main_image:
            return f'<img src="{obj.main_image.url}" style="max-height: 50px;" />'
        return _("Нет изображения")

    main_image_preview.allow_tags = True
    main_image_preview.short_description = _('Превью')

    #def save_model(self, request, obj, form, change):
        #"""Автоматическое сохранение slug, если он пустой"""
        #if not obj.slug:
         #   obj.slug = obj._meta.get_field('slug').generate_slug(obj)
       # super().save_model(request, obj, form, change)