from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductFilterView  # Новое представление
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('filter/', ProductFilterView.as_view(), name='product_filter'),  # Новый путь
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]