"""
Define views and constraints for each view.
"""

import collections
import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core import serializers

from .models import Category, Product, ProductImage, ProductCountdown

# Create your views here.


class SubcategoryIndex:  # pylint: disable=too-few-public-methods
    """Used to get index of subcategory."""

    index = 0
    index1 = 0


def home(request):
    """Define the Home display function."""

    SubcategoryIndex.index = 0
    SubcategoryIndex.index1 = 0
    category_object = Category.objects.all()
    category_list = []
    subcategory_list = []
    category_dict = {}

    for category in category_object:
        if category.__str__().find('==') == -1:
            category_list.append(category.__str__())
            category_dict[category_list[-1]] = 0
        else:
            subcategory_list.append(category.__str__())

    subcategory_list = sorted(subcategory_list)
    category_list = sorted(category_list)
    category_dict = dict(collections.OrderedDict(
        sorted(category_dict.items())))

    count = 0
    for category in subcategory_list:
        subcategory_list[count] = str(subcategory_list[count]).split(' ==> ')
        category_dict[category.split(' ==> ')[0]] += 1
        count += 1

    products_top_trending = Product.objects.all()[:8]

    products_new_arrival = Product.objects.all().order_by('-id')[:10]

    product_countdown = ProductCountdown.objects.all()[:2]

    context = {
        'categories': category_list,
        'category_dict': category_dict,
        'subcategory_list': list(subcategory_list),
        'products_top_trending': products_top_trending,
        'product_countdown': product_countdown,
        'products_new_arrival': products_new_arrival,
        'val': "False",
    }
    return render(request, 'index.html', context)


def product_quick_view(request, id):
    product = get_object_or_404(Product, id=id)
    product_images = ProductImage.objects.filter(product=product)
    product_images_json = serializers.serialize("json", product_images)
    product_images_object = json.loads(product_images_json)

    context = {
        'product_title': product.title,
        'product_price': product.price,
        'product_image': product.image_url,
        'product_description': product.description,
        'product_sale_price': product.sale_price,
        'product_images': product_images_object,
        'category_list': product.get_cat_list,
    }
    return JsonResponse(context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_images = ProductImage.objects.filter(product=product)

    context = {
        'product': product,
        'product_images': product_images,
    }
    return render(request, 'product-detail.html', context)
