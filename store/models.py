from django.db import models
from authentication.models import UserModel
from django.utils.text import slugify
from .utils import validate_score
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ('available', 'Available'),
    ('out_of_stock', 'Out of Stock'),
    ('discontinued', 'Discontinued'),
]

TYPE_CHOICES = [
    ('men', 'Men'),
    ('women', 'Women'),
    ('baby', 'Baby'),
]


class BrandModel(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    slug = models.SlugField(_("slug"), max_length=50, unique=True, blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "brand"
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


class CategoryModel(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=100, unique=True, blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = 'category'


class ProductModel(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=100, unique=True, editable=False, )
    description = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to='products/', blank=True, null=True)

    real_price = models.DecimalField(_("real price"), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(_("discount price"), max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(_("discount"), max_digits=5, decimal_places=2, default=0)

    is_on_sale = models.BooleanField(_("is on sale"), default=False)
    sale_start_date = models.DateField(_("sale start date"), blank=True, null=True)
    sale_end_date = models.DateField(_("sale end date"), blank=True, null=True)

    stock = models.PositiveIntegerField(_("stock"), default=0)
    sold = models.PositiveIntegerField(_("sold"), default=0)
    status = models.CharField(_("status"), max_length=15, choices=STATUS_CHOICES, default='available', )

    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(BrandModel, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='men')

    is_featured = models.BooleanField(_("is featured"), default=False)
    is_new = models.BooleanField(_("is new"), default=False)

    month_of_deal = models.BooleanField(_("month of deal"), default=False)
    deal_start_date = models.DateField(_("deal start date"), blank=True, null=True)
    deal_end_date = models.DateField(_("deal end date"), blank=True, null=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if self.discount and self.discount > 0:
            self.discount_price = self.real_price - (self.real_price * self.discount / 100)
        else:
            self.discount_price = self.real_price

        if self.stock <= 0:
            self.status = 'out_of_stock'
        else:
            self.status = 'available'

        if self.created_at and self.created_at >= timezone.now() - timedelta(days=3):
            self.is_new = True
        else:
            self.is_new = False

        super().save(*args, **kwargs)

    @property
    def display_price(self):
        return self.discount_price if self.discount > 0 else self.real_price

    @property
    def sold_percent(self):
        if self.stock - self.sold >= 0:
            return (self.sold * 100) / self.stock
        return 0

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        db_table = 'product'


class RatingModel(models.Model):
    product = models.ForeignKey(ProductModel, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    rating = models.FloatField(_("rating"), validators=[validate_score])
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        db_table = 'rating'


class ProductResultModel(models.Model):
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE, related_name='result')
    overall_rating = models.FloatField(_("overall rating"), default=0.0)

    def calculate_overall_rating(self):
        ratings = self.product.ratings.all()
        if ratings.exists():
            total = sum([rating.rating for rating in ratings])
            self.overall_rating = total / ratings.count()
        else:
            self.overall_rating = 0.0
        self.save()

    def __str__(self):
        return f"Overall rating for {self.product.name}: {self.overall_rating:.2f}"

    class Meta:
        verbose_name = _("Product Result")
        verbose_name_plural = _("Product Results")
        db_table = 'product_results'


class WishlistModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="wishlists", blank=True, null=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"

    @classmethod
    def product_count(cls, user):
        return cls.objects.filter(user=user).count()

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")
        db_table = 'wishlist'


class CartModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"), default=1)

    is_ordered = models.BooleanField(_("is ordered"), default=False)

    date_added = models.DateTimeField(_("date added"), auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @staticmethod
    def total_items(user):
        return CartModel.objects.filter(user=user).aggregate(Sum('quantity'))['quantity__sum'] or 0

    def total_price(self):
        base_price = self.product.real_price

        if self.product.discount:
            discount_price = base_price * (1 - self.product.discount / 100)
        else:
            discount_price = base_price
        return discount_price * self.quantity

    @staticmethod
    def cart_total_price(user):
        total = 0
        for item in CartModel.objects.filter(user=user):
            total += item.total_price()
        return total

    class Meta:
        db_table = 'cart'
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
