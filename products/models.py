from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=100)
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=100, blank=True, null=True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
