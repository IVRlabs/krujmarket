# Стандартные импорты Django
from autoslug.settings import slugify
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Сторонние библиотеки
from autoslug import AutoSlugField
from meta.models import ModelMeta

from django.utils.text import slugify



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
        editable=True,
        blank=True,
        null=True,
    )


    description = models.TextField(
        blank=True,
        verbose_name=_("Описание"),
        help_text=_("Необязательное поле")
    )

    #def save(self, *args, **kwargs):
    #    if not self.slug:
     #       self.slug = slugify(self.name)
      #  super().save(*args, **kwargs)



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
    """
    # Основные поля товара
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

    # Поле для главного изображения (переименовано из image в main_image для ясности)
    main_image = models.ImageField(
        upload_to="products/main/",
        verbose_name=_("Главное изображение"),
        help_text=_("Основное фото товара (рекомендуемый размер: 800x800px)"),
        default="products/main/images.png"
    )

    # Статусы и даты
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активный"),
        help_text=_("Отображать товар в каталоге?")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )
    is_featured = models.BooleanField(
        'Рекомендуемый',
        default=False,
        help_text=_("Показывать товар в рекомендуемых?")
    )

    # SEO-поля
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

    # Новые поля ==============================================
    available = models.BooleanField(
        "В наличии",
        default=True,
        help_text=_("Отметьте, если товар есть в наличии")
    )
    is_custom = models.BooleanField(
        "Эксклюзивный заказ",
        default=False,
        help_text=_("Если товар изготавливается индивидуально")
    )

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


class ProductImage(models.Model):
    """
    Модель для дополнительных изображений товара.
    Связана с Product через ForeignKey.
    Позволяет загружать несколько изображений для одного товара.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images',  # Используем related_name для доступа из Product
        verbose_name=_("Товар")
    )
    image = models.ImageField(
        upload_to='products/gallery/',
        verbose_name=_("Изображение"),
        help_text=_("Дополнительное фото товара")
    )
    alt_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Alt-текст"),
        help_text=_("Описание изображения для SEO")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Порядок сортировки"),
        help_text=_("Чем меньше число, тем выше фото в галерее")
    )

    class Meta:
        verbose_name = _("Дополнительное изображение")
        verbose_name_plural = _("Дополнительные изображения")
        ordering = ['order']

    def __str__(self):
        return f"Изображение #{self.order} для {self.product.name}"