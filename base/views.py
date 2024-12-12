from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from store.models import ProductModel, CategoryModel, ProductResultModel, RatingModel, CartModel, WishlistModel
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

TYPE_CHOICES = [
    ('men', 'Men'),
    ('women', 'Women'),
    ('baby', 'Baby'),
]

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 4)
    paginated_products = paginator.get_page(page)

    categories = CategoryModel.objects.all()

    d = {
        'products': paginated_products,
        'type_choices': TYPE_CHOICES,
        'search_query': search_query,
        'category_filter': category_filter,
        'type_filter': type_filter,
        'sort_by': sort_by,
        'categories': categories,
    }
    return render(request, 'store/shop.html', context=d)

@login_required(login_url='/accounts/login/')
def product_view(request, slug):
    product = get_object_or_404(ProductModel, slug=slug)

    product_result, created = ProductResultModel.objects.get_or_create(product=product)
    if created:
        product_result.save()

    overall_rating = product_result.overall_rating

    if request.method == 'POST':
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

        elif 'add_to_wishlist' in request.POST:
            if WishlistModel.objects.filter(user=request.user, product=product).exists():
                messages.info(request, "This product is already in your wishlist.")
            else:
                WishlistModel.objects.create(user=request.user, product=product)
                messages.success(request, f"{product.name} added to your wishlist!")

            return redirect('base:product', slug=slug)

        elif 'rating' in request.POST:
            try:
                rating_value = float(request.POST.get('rating'))
                if not (1 <= rating_value <= 5):
                    messages.error(request, "Rating must be between 1 and 5.")
                    return redirect('base:product', slug=slug)

                RatingModel.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={'rating': rating_value}
                )

                product_result.calculate_overall_rating()
                product_result.save()

                messages.success(request, "Rating submitted successfully!")
                return redirect('base:product', slug=slug)

            except ValueError:
                messages.error(request, "Invalid rating value.")
                return redirect('base:product', slug=slug)

    user_rating = None
    if request.user.is_authenticated:
        user_rating = product.ratings.filter(user=request.user).first()

    context = {
        'product': product,
        'overall_rating': overall_rating,
        'user_rating': user_rating or None,
    }

    return render(request, 'store/product.html', context)
