from django.shortcuts import render, redirect
from django.utils.translation import activate
from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'home.html', context=context)
