"""
Configure the administrator for both Order and Book.
"""

from django.contrib import admin

from .models import Product, ProductImage, Category

# Register your models here.


class InlineProductImage(admin.StackedInline):
    """display Model of ProductImage with some modifications to its functionality."""

    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """display Model of Product with some modifications to its functionality."""

    search_fields = ['title', 'description']
    list_display = ['title', 'price', 'active', 'update']
    list_filter = ['active']
    readonly_fields = ['timestamp', 'update']
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['slug', ]
    inlines = [InlineProductImage]

    class Meta:  # pylint: disable=too-few-public-methods
        """Define the class name of the model"""
        model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """display Model of Category with some modifications to its functionality."""

    def get_form(self, request, obj=None, **kwargs):
        category_object = Category.objects.all()
        category_list = []
        count = 1
        for category in category_object:
            if len(category.__str__().split(' ==> ')) < 3:
                category_list.append(count)
            count += 1
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = Category.objects.filter(
            id__in=category_list)
        return form

    readonly_fields = ['slug', ]

    class Meta:  # pylint: disable=too-few-public-methods
        """Define the class name of the model"""
        model = Category


admin.site.register(ProductImage)
