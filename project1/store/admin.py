from django.contrib import admin
from .models import Product, ProductImage
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category',
                    'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
