from django.contrib import admin

from .models import Product, ProductImage

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    search_fields = ['title', 'description']
    list_display = ['title', 'price', 'active', 'update']
    list_filter = ['active']
    readonly_fields = ['timestamp', 'update']
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Product


admin.site.register(ProductImage)
