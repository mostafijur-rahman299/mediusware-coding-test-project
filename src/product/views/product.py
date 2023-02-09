from django.views import generic

from product.models import Variant, Product


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'product_list'
    paginate_by = 2
    
    def get_queryset(self):
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['product'] = True
        
        print(dir(context['page_obj']))
        return context
    

