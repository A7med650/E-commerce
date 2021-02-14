"""
Configure the model for both Product and Category.
"""

from django.db import models
from django.utils.text import slugify
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from froala_editor.fields import FroalaField

# Create your models here.


def rename_image(instance, filename):
    """this function rename image before saving."""

    extension = filename.split('.')[-1]
    image_name = "product-images/{}.{}".format(
        instance.title+'-'+str(instance.id), extension)
    return image_name


def rename_product_image(instance, filename):
    """this function rename image before saving."""

    extension = filename.split('.')[-1]
    image_name = "product-images/{}.{}".format(
        instance.product.title+'-'+str(instance.id), extension)
    return image_name


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True)
    full_path_category = models.CharField(
        max_length=2000, null=True, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' ==> '.join(full_path[::-1])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name) + "-" + \
            str(urlsafe_base64_encode(force_bytes(self.id)))
        self.full_path_category = self.__str__()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Product(models.Model):
    """Model definition for Product."""

    title = models.CharField(max_length=100)
    description = FroalaField(theme='gray')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)
    image = models.ImageField(null=True, upload_to=rename_image)
    slug = models.SlugField(unique=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        """this function check if it image is none or not."""

        url = self.image.url
        if url is None:
            url = ''
        return url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title) + "-" + \
            str(urlsafe_base64_encode(force_bytes(self.id)))
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    @property
    def get_cat_list(self):
        """this function to get category in list."""

        k = self.category  # for now ignore this instance method
        breadcrumb = ['Ahmed']
        while k is not None:
            breadcrumb.append(k.name)
            k = k.parent
        # for i in range(len(breadcrumb)-1):
        #     breadcrumb[i] = ' ==> '.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]


class ProductImage(models.Model):
    """Model definition for ProductImage."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=rename_product_image)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    @property
    def image_url(self):
        """this function check if it image is none or not."""

        url = self.image.url
        if url is None:
            url = ''
        return url


class ProductCountdown(models.Model):
    """Model definition for ProductCountdown."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title
