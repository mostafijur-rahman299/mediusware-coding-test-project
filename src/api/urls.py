from django.urls import path

from api.views import product_create_view


urlpatterns = [
    path("create-product/", product_create_view, name="product_create_view"),
]

