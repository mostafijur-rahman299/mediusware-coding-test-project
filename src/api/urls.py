from django.urls import path

from api.views import product_create_view, product_detail_view, product_update_view


urlpatterns = [
    path("create-product/", product_create_view, name="product_create_view"),
    path("product-info/<int:product_id>/", product_detail_view, name="product_detail_view"),
    path("update-product/<int:product_id>/", product_update_view, name="product_update_view"),
]

