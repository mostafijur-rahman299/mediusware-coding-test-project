from django.urls import path, include

from product.views.product import CreateProductView, ProductListView, UpdateProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('update/<int:product_id>/', UpdateProductView.as_view(), name='update.product'),
    path('list/', ProductListView.as_view(), name='list.product'),
    
    # Api URLs
    path("api/", include(("api.urls", "api"), namespace="api")),
]
