from django.urls import path
from .views import cart_view

app_name = 'store'

urlpatterns = [
    path('cart/', cart_view, name='cart')
]
