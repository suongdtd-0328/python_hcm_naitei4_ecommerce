from django.utils.translation import gettext as _
from django.contrib import admin
from .models import Product, ProductImage
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = (_('product_name'), _('price'), _('category'),
                    _('created_date'), _('modified_date'), _('is_available'))
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
