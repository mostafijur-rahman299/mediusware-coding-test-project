from django.contrib import admin

from product.models import Product, ProductVariant, ProductVariantPrice

admin.site.register([Product, ProductVariant, ProductVariantPrice])
