from django.db import models
from django.utils.translation import gettext_lazy as _
from category.models import Category


class Product(models.Model):
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name=_("Slug"))
    product_name = models.CharField(
        max_length=200, unique=True, verbose_name=_("Product_Name"))
    description = models.TextField(
        max_length=500, blank=True, verbose_name=_("Description"))
    price = models.IntegerField(verbose_name=_("Price"))
    is_available = models.BooleanField(
        default=True, verbose_name=_("Is_Available"))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created_Date"))
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name=_("Modified_Date"))

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("Category"))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product_image = models.ImageField(
        upload_to='photos/products', verbose_name=_("Product_Image"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Product"))

    class Meta:
        verbose_name = _('Product_Image')
        verbose_name_plural = _('Product_Images')

    def __str__(self):
        return f"{_('Image of')} {self.product.product_name}"
