"""Urls definition."""

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/', views.product_detail, name='product_detail'),
    path('product-quick-view/<id>',
         views.product_quick_view, name='product-quick-view'),
]
