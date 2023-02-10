from django.views import generic
from django.db.models import Q

from product.models import Variant, Product, ProductVariant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    

class UpdateProductView(generic.TemplateView):
    template_name = 'products/update.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        context['product_id'] = kwargs.get('product_id')
        return context


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'product_list'
    paginate_by = 10
    
    def get_queryset(self):
        all_products = Product.objects.all().order_by("-id")
        
        # Filtering data
        if self.request.GET.get('title'):
            all_products = all_products.filter(title__icontains=self.request.GET.get('title'))
        if self.request.GET.get('variant'):
            all_products = all_products.filter(productvariant__variant_title=self.request.GET.get('variant')).distinct()
        if self.request.GET.get('date'):
            all_products = all_products.filter(created_at__date=self.request.GET.get('date'))
            
        # Filtering products data according to price_from and/or price_to
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        if  price_from and price_to:
            all_products = all_products.filter(Q(productvariantprice__price__gte=price_from)&Q(productvariantprice__price__lte=price_to)).distinct()
        elif price_from and not price_to:
            all_products = all_products.filter(productvariantprice__price__gte=price_from).distinct()
        elif not price_from and price_to:
            all_products = all_products.filter(productvariantprice__price__lte=price_to).distinct()
        
        return all_products
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['product'] = True
        
        # Taking variant data as dict due to items and sub items selection feature
        variants = Variant.objects.all()
        variant_dict = {}
        for variant in variants:
            variant_dict[variant.title] = list(ProductVariant.objects.filter(variant=variant).values_list("variant_title", flat=True).distinct())
        context['variant_list'] = variant_dict
            
        return context
    
