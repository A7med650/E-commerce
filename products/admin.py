"""
Configure the administrator for both Order and Book.
"""

from django.contrib import admin

from .models import Product, ProductImage, Category, ProductCountdown, Logo

# Register your models here.


class InlineProductImage(admin.StackedInline):
    """display Model of ProductImage with some modifications to its functionality."""

    model = ProductImage
    max_num = 6
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """display Model of Product with some modifications to its functionality."""

    fieldsets = (
        (None, {
            "fields": (
                'title', 'description',
            ),
        }),
        ('Choose Category', {
            "fields": (
                'category',
            ),
        }),
        ('Price and Sale price', {
            "fields": (
                'price', 'sale_price',
            ),
        }),
        ('Prime Image', {
            "fields": (
                'image',
            ),
        }),
        (None, {
            "fields": (
                'active',
            ),
        }),
    )

    search_fields = ['title', 'description']
    list_display = ['title', 'price', 'active', 'update']
    list_filter = ['active']
    readonly_fields = ['timestamp', 'update']
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['slug', ]
    inlines = [InlineProductImage]

    def get_form(self, request, obj=None, **kwargs):
        category_object = Category.objects.all()
        category_list = []
        count = 1
        for category in category_object:
            if len(category.__str__().split(' ==> ')) > 1:
                category_list.append(count)
            count += 1
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['category'].queryset = Category.objects.filter(
            id__in=category_list).order_by('full_path_category')
        return form

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
    ordering = ('full_path_category',)

    class Meta:  # pylint: disable=too-few-public-methods
        """Define the class name of the model"""
        model = Category


@admin.register(ProductCountdown)
class ProductCountdownAdmin(admin.ModelAdmin):
    """display Model of ProductCountdown with some modifications to its functionality."""

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        product_chooser_remove = list(ProductCountdown.objects.values_list(
            'product', flat=True))
        form.base_fields['product'].queryset = Product.objects.filter(
            sale_price__isnull=False).exclude(id__in=product_chooser_remove)
        return form


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    """display Model of Logo with some modifications to its functionality."""

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if Logo.objects.count() > 0:
            return False
        return super().has_add_permission(request)


admin.site.register(ProductImage)
