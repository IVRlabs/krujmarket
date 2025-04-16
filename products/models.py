# Стандартные импорты Django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Сторонние библиотеки
from autoslug import AutoSlugField
from meta.models import ModelMeta

class Category(models.Model):
    """
    Модель категории товаров.
    Attributes:
        name (CharField): Название категории (макс. 100 символов).
        slug (AutoSlugField): ЧПУ-URL (автогенерация из `name`).
        description (TextField): Описание категории (необязательное).
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Название"),
        help_text=_("Например: Кольца, Серьги, Подвески")
    )
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        verbose_name=_("URL-адрес"),
        help_text=_("Автоматически генерируется из названия")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Описание"),
        help_text=_("Необязательное поле")
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["name"]  # Сортировка по имени

    def __str__(self):
        """Строковое представление объекта (для админки и консоли)."""
        return self.name

    def get_absolute_url(self):
        """URL для детальной страницы категории."""
        return reverse("category_detail", kwargs={"slug": self.slug})

class Product(ModelMeta, models.Model):
    """
    Модель товара (украшения) с поддержкой SEO-метатегов.
    Наследуется от ModelMeta для автоматического формирования meta-тегов.
    Attributes:
        name (CharField): Название товара.
        price (DecimalField): Цена (макс. 10 цифр, 2 знака после запятой).
        category (ForeignKey): Связь с моделью Category.
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_("Название"),
        help_text=_("Полное название товара")
    )
    slug = AutoSlugField(
        populate_from="name",
        editable=True,
        unique=True,
        verbose_name=_("URL-адрес")
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Подробное описание товара")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена"),
        help_text=_("Цена в рублях")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Категория")
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name=_("Изображение"),
        help_text=_("Рекомендуемый размер: 800x800px")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активный"),
        help_text=_("Отображать товар в каталоге?")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    # Поля для SEO
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        verbose_name=_("Мета-заголовок (SEO)"),
        help_text=_("Заголовок для поисковых систем (до 60 символов)")
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Мета-описание (SEO)"),
        help_text=_("Краткое описание для сниппета (до 160 символов)")
    )

    # Конфигурация django-meta
    _metadata = {
        "title": "meta_title",
        "description": "meta_description",
        "og_type": "product",
        "og_locale": "ru_RU",
    }

    is_featured = models.BooleanField('Рекомендуемый', default=False)  # Добавляем, если отсутствует

    objects = models.Manager()

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
        ordering = ["-created_at"]  # Сортировка по дате (новые сначала)
        indexes = [
            models.Index(fields=["slug"], name="product_slug_idx"),
            models.Index(fields=["price"], name="product_price_idx"),
        ]

    def __str__(self):
        """Строковое представление товара."""
        return f"{self.name} ({self.price} руб.)"

    def get_absolute_url(self):
        """URL для детальной страницы товара."""
        return reverse("product_detail", kwargs={"slug": self.slug})