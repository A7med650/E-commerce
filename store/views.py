from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import __cart_id
from carts.models import CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


def home(request):
    products = Product.objects.filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product, category__slug=category_slug, slug=product_slug)
    is_cart = CartItem.objects.filter(cart__cart_id=__cart_id(
        request), product=single_product).exists()
    context = {
        'single_product': single_product,
        'is_cart': is_cart,
    }
    return render(request, 'store/product-detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
