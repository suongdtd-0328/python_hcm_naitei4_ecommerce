from django.db import models
from category.models import Category

# Create your models here.


class Product(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product_image = models.ImageField(upload_to='photos/products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image of {self.product.product_name}"
