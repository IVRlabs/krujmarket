from .models import Cart

def cart(request):
    try:
        cart = Cart.objects.get_for_request(request)
        return {
            'cart': cart,
            'cart_total_items': cart.items.count()
        }
    except Cart.DoesNotExist:
        return {
            'cart': None,
            'cart_total_items': 0
        }