"""
URL configuration for jewelry_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# jewelry_shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace='products')),
    path('', include('pages.urls', namespace='pages')),
    path('cart/', include('cart.urls', namespace='cart')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""urlpatterns = [
    path('admin/', admin.site.urls),
    # Страницы (О нас, Контакты)
    path('', include('pages.urls')),
    # Товары (Каталог, Детали товара)
    path('products/', include('products.urls')),
]"""




"""urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  # Подключаем маршруты products
    path('', include('pages.urls')),
]"""