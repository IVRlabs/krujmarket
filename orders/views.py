from django.http import JsonResponse

from .models import Order

from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart


def create_order(request):
    try:
        cart = Cart.objects.get_for_request(request)
    except Cart.DoesNotExist:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        order_data = {
            'customer_name': request.POST.get('customer_name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email', ''),
            'items': cart.get_items_json(),
            'total': cart.total_price,
            'payment_type': request.POST.get('payment_type', 'full')
        }

        # Добавляем user/session только если они существуют
        if request.user.is_authenticated:
            order_data['user'] = request.user
        else:
            order_data['session_key'] = request.session.session_key

        order = Order.objects.create(**order_data)
        cart.items.all().delete()

        return JsonResponse({
            'status': 'success',
            'order_id': order.id
        })

    return render(request, 'orders/create_order.html', {
        'cart': cart,
        'has_in_stock_items': any(item.product.available for item in cart.items.all())
    })