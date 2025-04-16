from django.shortcuts import render, redirect

def cart_detail(request):
    return render(request, 'cart/detail.html')

def cart_add(request, product_id):
    # Логика добавления товара
    return redirect('cart:detail')

def cart_remove(request, product_id):
    # Логика удаления товара
    return redirect('cart:detail')