from django.urls import path
from . import views
from .views import cart_summary

app_name = 'cart'  # Пространство имен для URL

urlpatterns = [
    # Основные URL
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    # API-эндпоинты
    path('api/count/', views.cart_count_api, name='cart_count_api'),
    path('api/summary/', views.cart_summary, name='cart_summary'),
]