from rest_framework import serializers
from product.models import Product, ProductImage, ProductVariant, ProductVariantPrice


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("id", "sku", "title", "description", )
        

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ("id", "file_path", )
        
        
class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ("id", "variant_title", )
        

class ProductVariantPriceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductVariantPrice
        fields = ("id", "title", "", )
        
        
        
