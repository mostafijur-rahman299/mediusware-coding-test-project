import json
import os
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import F, Value, Func

from api.serializers import ProductSerializer
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


@api_view(["GET",])
@permission_classes([permissions.AllowAny])
def product_detail_view(request, product_id):
    product_obj = Product.objects.filter(id=product_id).first()
    if not product_obj:
        return Response({"error": "Product not found"}, status=400)
    
    data = {}
    data["product_details"] = ProductSerializer(product_obj).data
    
    # Format product variant data for display update page
    variants = product_obj.productvariant_set.values_list("variant__id", flat=True).distinct()
    product_variants = []
    for variant in variants:
        tags = product_obj.productvariant_set.filter(variant__id=variant).values_list("variant_title", flat=True)
        product_variants.append({"option": variant, "tags": tags})
    
    data["product_variants"] = product_variants
    
    # Format product variant price data for display update page
    product_variant_price_data = []
    product_variant_prices = product_obj.productvariantprice_set.all()
    for product_variant_price in product_variant_prices:
        
        title = ""
        if product_variant_price.product_variant_one:
            title = f"{product_variant_price.product_variant_one.variant_title}/"
        if product_variant_price.product_variant_two:
            title = title + f"{product_variant_price.product_variant_two.variant_title}/"
        if product_variant_price.product_variant_three:
            title = title + f"{product_variant_price.product_variant_three.variant_title}/"
            
        product_variant_price_data.append({"title": title, "price": product_variant_price.price, "stock": product_variant_price.stock})
        
    data['product_variant_prices'] = product_variant_price_data
    
    return Response(data)


@api_view(["put",])
@permission_classes([permissions.AllowAny])
def product_update_view(request, product_id):
    
    product_obj = Product.objects.filter(id=product_id).first()
    if not product_obj:
        return Response({"error": "Product not found"}, status=400)
    
    # Update product data
    product_data = json.loads(request.POST.get("product_details"))
    product_obj.title = product_data.get("title")
    product_obj.sku = product_data.get("sku")
    product_obj.description = product_data.get("description")
    product_obj.save()
    
    # Save Product Image
    product_image = request.FILES.get("product_image")
    if product_image:
        server_file_location = os.path.join(settings.MEDIA_ROOT, "product-image/")  # Where save the file
        fs = FileSystemStorage(location=server_file_location)
        filename = fs.save(f"{product_image.name}", product_image)
        final_file_path = settings.MEDIA_URL + filename  # file path
        
        # If already exists then update otherwise create new one
        img_instance = ProductImage.objects.filter(product=product_obj).first()
        if img_instance:
            img_instance.file_path = final_file_path
        else:
            product_image_instance = ProductImage(**{"file_path": final_file_path})
            product_image_instance.product = product_obj
            product_image_instance.save()
            
    # Update Product Variants
    product_variants = json.loads(request.POST.get("product_variants"))
    ProductVariant.objects.filter(product=product_obj).delete() # Delete Previous data
    for product_variant in product_variants:
        option = product_variant.get("option")
        option = Variant.objects.filter(id=option).first()
        if option:
            # Create/Update product variant
            tags = product_variant.get("tags")
            for tag in tags:
                product_variant_instance = ProductVariant(**{"variant_title": tag})
                product_variant_instance.variant = option
                product_variant_instance.product = product_obj
                product_variant_instance.save()
                    
    
    # Save Product Variant Prices data
    ProductVariantPrice.objects.filter(product=product_obj).delete() # Delete all previous data
    product_variant_prices = json.loads(request.POST.get('product_variant_prices'))
    for product_variant_price in product_variant_prices:
        variants = product_variant_price.get("title").split("/")
        variants = variants[:len(variants) - 1]
        price = product_variant_price.get("price")
        stock = product_variant_price.get("stock")
        product_variant_price_instance = ProductVariantPrice(price=price, stock=stock, product=product_obj)
        
        product_variant_price_type = ["product_variant_one", "product_variant_two", "product_variant_three"]
        # Dynamically added product variant to product variant price object.
        for field_name, variant in zip(product_variant_price_type, variants):
            variant_obj = ProductVariant.objects.filter(variant_title=variant).first()
            product_variant_price_instance.__setattr__(field_name, variant_obj)
            
        product_variant_price_instance.save()
    
    return Response({})
