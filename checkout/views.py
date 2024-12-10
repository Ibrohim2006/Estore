from itertools import product

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import CartModel
from .forms import OrderForm
from .models import CouponModel, OrderModel  # Assuming OrderModel exists


def checkout_view(request):
    discount_amount = 0
    # Retrieve the active cart for the logged-in user
    cart_items = CartModel.objects.filter(user=request.user)

    # If no active cart is found, show an error message
    if not cart_items:
        messages.error(request, "You have no active cart.")
        return redirect('store:cart')

    if request.method == 'POST':
        print('*' * 100)
        print(request.POST['coupon'])
        print('*' * 100)
        if request.POST['coupon'] == '':
            coupon = CouponModel.objects.filter(code=request.POST['coupon']).first()
            cart_total = sum(item.total_price() for item in cart_items)

            order = OrderModel.objects.create(
                user=request.user,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                city=request.POST['city'],
                country=request.POST['country'],
                quantity=CartModel.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum'],
                price=int(cart_total)
            )

            order.product_name.set(CartModel.objects.filter(user=request.user).values_list('product', flat=True))

            order.save()
            for cart_item in cart_items:
                cart_item.product.is_featured = True
                cart_item.product.save()
            cart_items.delete()

            return redirect('checkout:checkout')
        else:
            coupon = CouponModel.objects.filter(code=request.POST['coupon']).first()
            if coupon is not None:
                cart_total = sum(item.total_price() for item in cart_items)

                order = OrderModel.objects.create(
                    user=request.user,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    phone=request.POST['phone'],
                    address=request.POST['address'],
                    city=request.POST['city'],
                    country=request.POST['country'],
                    coupon=CouponModel.objects.filter(code=request.POST['coupon']).first(),
                    quantity=CartModel.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum'],
                    price=int(cart_total) - ((int(cart_total) * coupon.discount) / 100)
                )

                order.product_name.set(CartModel.objects.filter(user=request.user).values_list('product', flat=True))

                order.save()
                for cart_item in cart_items:
                    cart_item.product.is_featured = True
                    cart_item.product.save()
                cart_items.delete()

                return redirect('checkout:checkout')
            else:
                messages.error(request, 'This coupon does not exist.')
                cart_items_with_totals = []
                subtotal = 0
                for item in cart_items:
                    total_price = item.product.display_price * item.quantity
                    cart_items_with_totals.append({
                        'item': item,
                        'total_price': total_price
                    })
                    subtotal += total_price

                shipping_cost = 10
                total = subtotal + shipping_cost

                d = {
                    'cart_items_with_totals': cart_items_with_totals,
                    'order': {
                        'subtotal': subtotal,
                        'shipping_cost': shipping_cost,
                        'total': total,
                    },
                }

                return render(request, 'checkout/checkout.html', context=d)

    else:
        cart_items_with_totals = []
        subtotal = 0
        for item in cart_items:
            total_price = item.product.display_price * item.quantity
            cart_items_with_totals.append({
                'item': item,
                'total_price': total_price
            })
            subtotal += total_price

        shipping_cost = 10
        total = subtotal + shipping_cost

        d = {
            'cart_items_with_totals': cart_items_with_totals,
            'order': {
                'subtotal': subtotal,
                'shipping_cost': shipping_cost,
                'total': total,
            },
        }

        return render(request, 'checkout/checkout.html', context=d)
