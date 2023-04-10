from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    category_name = models.CharField(
        max_length=50, unique=True, verbose_name=_('Category Name'))
    description = models.TextField(
        max_length=255, blank=True, verbose_name=_('Description'))
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(
        upload_to='photos/categories/', blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
