from django.urls import path
from .views import index_view, shop_view, product_view, search_view

app_name = 'base'
urlpatterns = [
    path('', index_view, name='index'),
    path('shop/', shop_view, name='shop'),
    path('products/<slug:slug>/', product_view, name='product'),
    path('search/', search_view, name='search'),
]
