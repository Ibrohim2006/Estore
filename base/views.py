from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from store.models import ProductModel, CategoryModel, ProductResultModel, RatingModel, CartModel, WishlistModel
from django.contrib import messages

TYPE_CHOICES = [
    ('men', 'Men'),
    ('women', 'Women'),
    ('baby', 'Baby'),
]


def index_view(request):
    products = ProductModel.objects.all()

    top_selling_products = sorted(
        products,
        key=lambda product: product.sold_percent,
        reverse=True
    )[:3]

    featured_products = ProductModel.objects.filter(is_featured=True)[:6]
    best_deals = ProductModel.objects.filter(month_of_deal=True).order_by('-created_at')[:3]

    context = {
        'top_selling_products': top_selling_products,
        'new_products': products,
        'featured_products': featured_products,
        'best_deals': best_deals,
    }

    return render(request, 'index.html', context)


def shop_view(request):
    products = ProductModel.objects.all().select_related('result')

    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category__name=category_filter)

    type_filter = request.GET.get('type', '')
    if type_filter:
        products = products.filter(type=type_filter)

    sort_by = request.GET.get('select', 'highest-rate')
    if sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'price':
        products = products.order_by('real_price')
    elif sort_by == 'highest_rated':
        products = sorted(products, key=lambda p: p.result.overall_rating if hasattr(p, 'result') else 0.0,
                          reverse=True)

    categories = CategoryModel.objects.all()

    d = {
        'products': products,
        'type_choices': TYPE_CHOICES,
        'search_query': search_query,
        'category_filter': category_filter,
        'type_filter': type_filter,
        'sort_by': sort_by,
        'categories': categories,
    }
    return render(request, 'store/shop.html', context=d)


def product_view(request, slug):
    product = get_object_or_404(ProductModel, slug=slug)

    # Get or create the product result (for overall rating calculation)
    product_result, created = ProductResultModel.objects.get_or_create(product=product)
    if created:
        product_result.save()

    overall_rating = product_result.overall_rating

    if request.method == 'POST':
        # Handle "Add to Cart"
        if 'quantity' in request.POST:
            try:
                quantity = int(request.POST.get('quantity', 1))
                if quantity < 1:
                    messages.error(request, "Quantity must be greater than zero.")
                    return redirect('base:product', slug=slug)

                cart_item, created = CartModel.objects.get_or_create(
                    user=request.user, product=product
                )
                if created:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity
                cart_item.save()

                messages.success(request, f"{product.name} added to your cart!")
                return redirect('base:product', slug=slug)

            except ValueError:
                messages.error(request, "Invalid quantity.")
                return redirect('base:product', slug=slug)

        # Handle "Add to Wishlist"
        elif 'add_to_wishlist' in request.POST:
            # Check if the product is already in the wishlist
            if WishlistModel.objects.filter(user=request.user, product=product).exists():
                messages.info(request, "This product is already in your wishlist.")
            else:
                # Add the product to the wishlist
                WishlistModel.objects.create(user=request.user, product=product)
                messages.success(request, f"{product.name} added to your wishlist!")

            return redirect('base:product', slug=slug)

        # Handle Rating
        elif 'rating' in request.POST:
            try:
                rating_value = float(request.POST.get('rating'))
                if not (1 <= rating_value <= 5):
                    messages.error(request, "Rating must be between 1 and 5.")
                    return redirect('base:product', slug=slug)

                # Create or update the user's rating for the product
                RatingModel.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={'rating': rating_value}
                )

                # Recalculate the overall rating of the product
                product_result.calculate_overall_rating()
                product_result.save()

                messages.success(request, "Rating submitted successfully!")
                return redirect('base:product', slug=slug)

            except ValueError:
                messages.error(request, "Invalid rating value.")
                return redirect('base:product', slug=slug)

    # Get the user's rating for the product
    user_rating = product.ratings.filter(user=request.user).first()

    context = {
        'product': product,
        'overall_rating': overall_rating,
        'user_rating': user_rating or None,
    }

    return render(request, 'store/product.html', context)


def search_view(request):
    search_query = request.GET.get('search', '')
    results = ProductModel.objects.filter(name__icontains=search_query)

    context = {
        'search': search_query,
        'products': results,
    }
    return render(request, 'search.html', context=context)