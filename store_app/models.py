from django.db import models
from django.core.exceptions import ValidationError

import re
import datetime
from decimal import Decimal

from .fields import *


"""
    Global Model: Manages global properties that may change with time, for example the relation US - MX value
"""


class GlobalModel(models.Model):
    active = models.BooleanField(default=False)
    mx_value = CurrencyDecimalField()
    us_sales_taxes = CurrencyDecimalField()
    last_updated = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.last_updated.strftime('%Y-%m-%d %H:%M') + " " + str(self.active)


"""
    Color model
"""


def custom_color_format_validator(value):
    if len(value) < 4:
        raise ValidationError("This field requires at least 4 characters")
    regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{8})$"
    if not re.search(re.compile(regex), value):
        raise ValidationError("This field is only from [0-9] and [a-f]")
    return value


class CustomColor(models.Model):
    nickname = models.CharField(max_length=50, default='Color Nickname', unique=True)
    code = models.CharField(max_length=9, default="#000000", validators=[custom_color_format_validator])

    def __str__(self):
        return self.nickname + " - " + self.code


"""
    Collection model. A collection contains a name and a year as unique 
"""


class ClothingCollection(models.Model):
    title = models.CharField(max_length=256, default='')
    year = models.CharField(max_length=4, default='2022')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/collections/', blank=True, null=True)

    def __str__(self):
        return self.title + " " + self.year

    def get_products_set(self):
        return self.clothing_products.all()

    @property
    def count_products_set(self):
        return self.clothing_products.count()


"""
    Category model. A category contains a name as unique 
"""


class Category(models.Model):
    title = models.CharField(max_length=256, default='', unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_products_set(self):
        return self.clothing_products.all()

    @property
    def count_products_set(self):
        return self.clothing_products.count()


"""
     Clothing Product Model
"""


class ClothingProduct(models.Model):
    name = models.CharField(max_length=256, default='', unique=True)
    code = models.CharField(max_length=50, default='')
    collections = models.ManyToManyField(ClothingCollection, related_name="clothing_products",
                                         related_query_name="clothing_products")
    categories = models.ManyToManyField(Category, related_name="clothing_products",
                                        related_query_name="clothing_products")
    available_colors = models.ManyToManyField(CustomColor, related_name="clothing_products",
                                              related_query_name="clothing_products")

    tag = models.CharField(max_length=50, choices=TAG_OPTIONS, default='SHIRT')

    base_pricing = CurrencyDecimalField()
    amount_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.code

    def pricing_with_tax(self):
        global_model = GlobalModel.objects.get(active=True)
        pricing_after_taxes = self.base_pricing + (self.base_pricing * global_model.us_sales_taxes)
        return Decimal(pricing_after_taxes)

    def pricing_with_tax_mx(self):
        global_model = GlobalModel.objects.get(active=True)
        mx_pricing_tax = self.pricing_with_tax() * global_model.mx_value
        return Decimal(mx_pricing_tax)

    def pricing_mx(self):
        global_model = GlobalModel.objects.get(active=True)
        mx_pricing_tax = self.base_pricing * global_model.mx_value
        return Decimal(mx_pricing_tax)

    def primary_image(self):
        return ClothingProductImage.objects.get(type_of_image="PRIMARY", product=self).image


class ClothingProductImage(models.Model):
    image = models.ImageField(upload_to='uploads/products/')
    type_of_image = models.CharField(max_length=50, choices=IMAGE_CHOICES, default='EXTRA')
    product = models.ForeignKey(ClothingProduct, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + " " + self.type_of_image


class Cart(models.Model):
    total_amount = CurrencyDecimalField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField()
    token = models.CharField(max_length=256, default='', blank=True)

    def __str__(self):
        return str(self.created_date) + " " + "Activo" if (self.is_active) else "Inactivo" + " " + str(self.total_amount)


class ProductVariation(models.Model):
    product = models.ForeignKey(ClothingProduct, on_delete=models.CASCADE)
    principal_color = models.ForeignKey(CustomColor, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, default='S')
    sleeve = models.CharField(max_length=50, default='None', blank=True)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product.name + " " + self.principal_color.nickname + " " + str(self.quantity)
