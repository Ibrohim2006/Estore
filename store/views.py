from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from .models import CartModel, WishlistModel
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def cart_view(request):
    cart_items = CartModel.objects.filter(user=request.user)

    cart_num = cart_items.count()

    cart_total = sum(item.total_price() for item in cart_items)
    cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    if request.method == 'POST':
        if 'update_quantity' in request.POST:
            try:
                product_id = request.POST.get('product_id')
                new_quantity = int(request.POST.get('quantity', 1))
                if new_quantity < 1:
                    messages.error(request, "Quantity must be at least 1.")
                else:
                    cart_item = CartModel.objects.get(user=request.user, product_id=product_id)
                    cart_item.quantity = new_quantity
                    cart_item.save()
                    messages.success(request, f"Updated quantity for {cart_item.product.name}.")

            except CartModel.DoesNotExist:
                messages.error(request, "The specified cart item does not exist.")
            except ValueError:
                messages.error(request, "Invalid quantity entered.")
            return redirect('store:cart')

        elif 'remove_item' in request.POST:
            try:
                product_id = request.POST.get('product_id')
                cart_item = CartModel.objects.get(user=request.user, product_id=product_id)
                cart_item.delete()
                messages.success(request, f"Removed {cart_item.product.name} from your cart.")
            except CartModel.DoesNotExist:
                messages.error(request, "The specified cart item does not exist.")
            return redirect('store:cart')
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_total_quantity': cart_total_quantity,
        'cart_num': cart_num
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='/accounts/login/')
def wishlist_view(request):
    wishlist = WishlistModel.objects.filter(user=request.user)

    context = {
        'wishlist': wishlist,
    }
    return render(request, 'store/wishlist.html', context)


@login_required(login_url='/accounts/login/')
def remove_wishlist_view(request, item_id):
    if request.method == 'POST':
        wishlist_item = get_object_or_404(WishlistModel, id=item_id, user=request.user)
        wishlist_item.delete()
        return redirect('store:wishlist')
