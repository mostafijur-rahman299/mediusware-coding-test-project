import json
import os
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from api.serializers import ProductSerializer, ProductImageSerializer, ProductVariantSerializer
from product.models import Product, Variant, ProductVariant, ProductVariantPrice,ProductImage


@api_view(["POST",])
@permission_classes([permissions.AllowAny])
def product_create_view(request):
        
    # Save Product Data
    product_instance = Product(**json.loads(request.POST.get("product_details")))
    product_instance.save()
    
    # Save Product Image
    product_image = request.FILES.get("product_image")
    if product_image:
        server_file_location = os.path.join(settings.MEDIA_ROOT, "product-image/")  # Where save the file
        fs = FileSystemStorage(location=server_file_location)
        filename = fs.save(f"{product_image.name}", product_image)
        final_file_path = settings.MEDIA_URL + filename  # file path
        product_image_instance = ProductImage(**{"file_path": final_file_path})
        product_image_instance.product = product_instance
        product_image_instance.save()
    
    # Save Product Variants
    product_variants = json.loads(request.POST.get("product_variants"))
    for product_variant in product_variants:
        option = product_variant.get("option")
        option = Variant.objects.filter(id=option).first()
        if option:
            # Create product variant
            tags = product_variant.get("tags")
            for tag in tags:
                product_variant_instance = ProductVariant(**{"variant_title": tag})
                product_variant_instance.variant = option
                product_variant_instance.product = product_instance
                product_variant_instance.save()
                    
    # Save Product Variant Prices data
    product_variant_prices = json.loads(request.POST.get('product_variant_prices'))
    for product_variant_price in product_variant_prices:
        variants = product_variant_price.get("title").split("/")
        variants = variants[:len(variants) - 1]
        price = product_variant_price.get("price")
        stock = product_variant_price.get("stock")
        product_variant_price_instance = ProductVariantPrice(price=price, stock=stock, product=product_instance)
        
        product_variant_price_type = ["product_variant_one", "product_variant_two", "product_variant_three"]
        # Dynamically added product variant to product variant price object. 
        for field_name, variant in zip(product_variant_price_type, variants):
            variant_obj = ProductVariant.objects.filter(variant_title=variant).first()
            product_variant_price_instance.__setattr__(field_name, variant_obj)
            
        product_variant_price_instance.save()
    
    return Response({"success": "Product is created successfully"})


