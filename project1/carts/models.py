from django.db import models
from store.models import Product
from accounts.models import Account
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    cart_id = models.CharField(
        max_length=250, blank=True, verbose_name=_("Cart ID"))
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Date added"))
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name=_("Total"))

    def __str__(self):
        return str(self.cart_id)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")


class CartItem(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, verbose_name=_("Account"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, verbose_name=_("Cart"))
    quantity = models.IntegerField(verbose_name=_("Quantity"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def sub_total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = _("Cart item")
        verbose_name_plural = _("Cart items")
