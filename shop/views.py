from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from .models import Product, SliderImage
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
from .models import Order



# View to display all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


# Add a product to the cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Retrieve quantity from request or default to 1
    try:
        quantity = int(request.POST.get('quantity', 1))  # Ensure valid quantity
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity provided.")
        return redirect('shop:product_detail', id=product_id)

    # Add or update the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += quantity
    cart_item.save()

    messages.success(request, f"{quantity} x {product.name} added to your cart.")
    return redirect('shop:cart_detail')


# View to show the user's cart
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Fetch all items in the cart
    cart_items = cart.cart_items.all()

    # Calculate the total price for the cart
    cart_total = sum(item.get_subtotal() for item in cart_items)

    return render(
        request,
        'shop/cart_detail.html',
        {'cart_items': cart_items, 'cart_total': cart_total},
    )


# Checkout process
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    # Check if the cart is empty
    if not cart.cart_items.exists():
        messages.error(request, "Your cart is empty! Add items before checking out.")
        return redirect('shop:cart_detail')

    # Create an order from the cart
    order = Order.objects.create(user=request.user, cart=cart)

    # Clear the cart after creating the order
    cart.cart_items.all().delete()

    messages.success(request, f"Order placed successfully! Your order ID is {order.id}.")
    return render(request, 'shop/order_confirmation.html', {'order': order})


# User Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('shop:product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'shop/signup.html', {'form': form})


# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('shop:product_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'shop/login.html', {'form': form})


# User Logout
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('shop:login')


# Product Detail View
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})
#profile detail view
@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save profile and update email in the User model
            return redirect('shop:profile')  # Redirect to the same page after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'shop/profile.html', {'form': form, 'profile': profile})
def product_search(request):
    query = request.GET.get('query', '')
    if query:
    # Filter products by name or description
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.none()  # If no query, show no products

    return render(request, 'shop/product_list.html', {'products': products, 'query': query})
    
    
def product_list(request):
    # Fetch the latest 3 slider images
    slider_images = SliderImage.objects.all().order_by('-created_at')[:3]
    
    # Fetch products for different sections
    featured_products = Product.objects.filter(is_featured=True)  # Example filter for featured products
    best_selling_products = Product.objects.all().order_by('-sales')[:5]  # Example for best-selling products
    new_arrivals = Product.objects.all().order_by('-created_at')[:5]  # Newest products
    discounted_products = Product.objects.filter(discount__gt=0)  # Products with discount

    # Searching functionality
    query = request.GET.get('query', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'shop/product_list.html', {
        'slider_images': slider_images,
        'featured_products': featured_products,
        'best_selling_products': best_selling_products,
        'new_arrivals': new_arrivals,
        'discounted_products': discounted_products,
        'products': products,
        'query': query
    })
    
    


def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_sales = Order.objects.aggregate(total_sales=Sum('total_price'))['total_sales']

    return render(request, 'shop/admin/dashboard/index.html', {
        'total_products': total_products,
        'total_customers': total_orders,  # This could be users or orders
        'total_sales': total_sales
    })