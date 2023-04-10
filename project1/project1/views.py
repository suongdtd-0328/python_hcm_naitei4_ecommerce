from django.shortcuts import render, redirect
from django.utils.translation import activate
from store.models import Product, Category


def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.filter(parent=None)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'home.html', context=context)
