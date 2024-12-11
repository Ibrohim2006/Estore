from django.urls import path
from .views import cart_view, wishlist_view, remove_wishlist_view

app_name = 'store'

urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:item_id>/', remove_wishlist_view, name='remove_from_wishlist'),
]
