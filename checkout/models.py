from django.db import models
from authentication.models import UserModel
from store.models import ProductModel


class CouponModel(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveSmallIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Coupon {self.code} - {self.discount}%"

    def is_valid(self):
        from django.utils.timezone import now
        return self.is_active and self.valid_from <= now() <= self.valid_to

    class Meta:
        db_table = 'coupon'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    coupon = models.ForeignKey(CouponModel, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.ManyToManyField(ProductModel)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"


    @property
    def total_price(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
