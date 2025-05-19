from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(request):
    """
    Получает или создает корзину для текущего пользователя/сессии
    Возвращает объект корзины
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()  # Создаем сессию для анонимного пользователя
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


from django.views.decorators.http import require_POST
from django.http import JsonResponse


@require_POST
def add_to_cart(request, product_id):
    """Добавляет товар в корзину (AJAX-версия)"""
    cart = get_or_create_cart(request)

    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price': product.price, 'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({
            'success': True,
            'cart_total_items': cart.total_quantity,
            'message': f"{product.name} добавлен в корзину"
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Товар не найден'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def remove_from_cart(request, item_id):
    """
    Удаляет товар из корзины
    """
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Товар удален из корзины")
    return redirect('cart:cart_detail')


def update_quantity(request, item_id):
    """
    Обновляет количество товара в корзине
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Количество обновлено")
        else:
            cart_item.delete()
            messages.success(request, "Товар удален из корзины")

    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Отображает содержимое корзины
    """
    #print('!!!!!!!!!!!!!!!!!!!!!!!', request.session['cart'])
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product')  # Оптимизация запросов

    context = {
        'cart': cart,
        'items': items,
        'total': cart.total_price,
        'total_quantity': cart.total_quantity
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_count_api(request):
    """
    API для получения количества товаров в корзине (для AJAX)
    """
    cart = get_or_create_cart(request)
    return JsonResponse({
        'count': cart.total_quantity,
        'total': str(cart.total_price)
    })


def checkout(request):
    """Оформление заказа в рамках приложения cart"""
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста")
        return redirect('cart:cart_detail')

    # Логика оформления заказа
    return render(request, 'cart/checkout.html', {'cart': cart})



def cart_summary(request):
    """API для получения данных корзины"""
    cart = get_or_create_cart(request)
    return JsonResponse({
        'total_quantity': cart.total_quantity,
        'total_price': str(cart.total_price)
    })

from django.http import JsonResponse

def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    return JsonResponse({'status': 'success'})