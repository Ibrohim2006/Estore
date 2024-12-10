from django.contrib import admin
from .models import *

admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(BrandModel)
admin.site.register(RatingModel)
admin.site.register(ProductResultModel)
admin.site.register(CartModel)
admin.site.register(WishlistModel)
