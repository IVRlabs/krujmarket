# Стандартные импорты Django
from django.urls import path
from django.utils.translation import gettext_lazy as _

# Локальные импорты (представления текущего приложения)
from . import views
from .views import AboutView, ContactsView, BlogView
app_name = 'products'  # Пространство имён приложения
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),  # /products/
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),  # /products/кольцо/
]