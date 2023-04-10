from django.shortcuts import render, redirect
from django.utils.translation import activate
from store.models import Product, Category


def home(request):
    products = Product.objects.filter(
        is_available=True).order_by('-created_date')

    parent_categories = Category.objects.filter(parent=None)

    context = {
        'products': products,
        'parent_categories': parent_categories,
    }
    return render(request, 'home.html', context=context)
