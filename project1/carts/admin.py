from django.contrib import admin
from .models import Cart, CartItem
from django.utils.translation import gettext as _


class CartAdmin(admin.ModelAdmin):
    list_display = (_('cart_id'), _('date_added'),)


class CartItemAdmin(admin.ModelAdmin):
    list_display = (_('product'), _('cart'), _('quantity'), _('is_active'),)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
