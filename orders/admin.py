from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'payment_type', 'status', 'total', 'created_at')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('id', 'customer_name', 'phone', 'email')
    readonly_fields = ('items_list', 'created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        ('Основное', {
            'fields': ('customer_name', 'phone', 'email', 'comment')
        }),
        ('Платежи', {
            'fields': ('payment_type', 'total', 'prepayment', 'status')
        }),
        ('Данные', {
            'fields': ('items_list', 'created_at', 'updated_at')
        }),
    )