from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from store.models import Product
from category.models import Category
from django.db.models import Q
from carts.models import Cart, CartItem
from carts.views import _cart_id

# Create your views here.


def store(request, category_slug=None):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) | Q(
                price__icontains=query) | Q(description__icontains=query),
            is_available=True
        ).distinct()
    elif category_slug:
        category = Category.objects.filter(slug__contains=category_slug)
        products = Product.objects.filter(
            category__in=category, is_available=True)
    elif min_price and max_price:
        products = Product.objects.filter(price__range=(min_price, max_price))
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 3)
    paged_products = paginator.get_page(page)
    product_count = products.count()
    categories = Category.objects.filter(parent=None)

    context = {
        'categories': categories,
        'products': paged_products,
        'product_count': product_count,
        'search_query': query,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'store/store.html', context=context)


def product_detail(request, category_slug, product_slug=None):
    single_product = Product.objects.get(
        category__slug=category_slug, slug=product_slug)

    similar_products = Product.objects.filter(
        category=single_product.category.parent, is_available=True).exclude(id=single_product.id)[:4]

    in_cart = False
    if request.user.is_authenticated:
        current_user = request.user
        is_exists_cart_item = CartItem.objects.filter(
            product=single_product, account=current_user).exists()
        if is_exists_cart_item:
            in_cart = True
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=single_product)
            in_cart = True
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            pass

    context = {
        'single_product': single_product,
        'similar_products': similar_products,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context=context)
