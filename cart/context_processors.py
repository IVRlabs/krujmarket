from .models import Cart


def cart(request):
    """Добавляет данные корзины в контекст всех шаблонов"""
    cart_data = {'total_quantity': 0}

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        if request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()

    if cart:
        cart_data['total_quantity'] = sum(item.quantity for item in cart.items.all())

    return {'cart': cart_data}