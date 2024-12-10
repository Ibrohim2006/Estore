from django import forms
from .models import OrderModel, CouponModel


class OrderForm(forms.ModelForm):
    coupon_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter coupon code', 'class': 'form-control'}),
        label="Coupon Code"
    )

    class Meta:
        model = OrderModel
        fields = [
            'product_name',
            'quantity',
            'price',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'city',
            'country',
        ]
        widgets = {
            'product_name': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Full Address', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }

    def clean_coupon_code(self):
        code = self.cleaned_data.get('coupon_code')
        if code:
            try:
                coupon = CouponModel.objects.get(code=code)
                if not coupon.is_valid():
                    raise forms.ValidationError("The coupon is expired or inactive.")
            except CouponModel.DoesNotExist:
                raise forms.ValidationError("Invalid coupon code.")
        return code

    def save(self, commit=True):
        """
        Save the order and attach a coupon if a valid code is provided.
        """
        order = super().save(commit=False)
        coupon_code = self.cleaned_data.get('coupon_code')
        if coupon_code:
            try:
                coupon = CouponModel.objects.get(code=coupon_code)
                if coupon.is_valid():
                    order.coupon = coupon
            except CouponModel.DoesNotExist:
                order.coupon = None

        if commit:
            order.save()
            self.save_m2m()  # Save ManyToMany fields (e.g., product_name)
        return order
