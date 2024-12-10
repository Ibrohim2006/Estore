from django.contrib import admin
from .models import OrderModel, CouponModel

admin.site.register(OrderModel)
admin.site.register(CouponModel)
