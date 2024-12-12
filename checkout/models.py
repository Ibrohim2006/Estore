from django.db import models
from authentication.models import UserModel
from store.models import ProductModel
from django.utils.translation import gettext_lazy as _


class CouponModel(models.Model):
    code = models.CharField(_("code"), max_length=50, unique=True)
    discount = models.PositiveSmallIntegerField(_("discount"), default=0)
    valid_from = models.DateTimeField(_("valid from"))
    valid_to = models.DateTimeField(_("valid to"))

    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return f"Coupon {self.code} - {self.discount}%"

    def is_valid(self):
        from django.utils.timezone import now
        return self.is_active and self.valid_from <= now() <= self.valid_to

    class Meta:
        db_table = 'coupon'
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    coupon = models.ForeignKey(CouponModel, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.ManyToManyField(ProductModel)
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    price = models.FloatField(_("price"), default=0)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("email") )
    phone = models.CharField(_("phone"), max_length=20)
    address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=50)
    country = models.CharField(_("country"), max_length=50)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"


    @property
    def total_price(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'order'
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
