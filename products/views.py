from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins
from .models import Product, CartItem, Order, OrderItem
from .serializers import ProductSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, ProductForm, AddToCartForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F

def home(request):
    return render(request, 'home.html')

@api_view(['GET'])
def api_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

class ProductCreateView(mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@login_required
@never_cache
def products(request):
    product_list = Product.objects.all().order_by('name')
    paginator = Paginator(product_list, 6)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products.html', {'products': products})

@login_required
@never_cache
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    add_to_cart_form = AddToCartForm()

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity <= 0:
                messages.error(request, "Quantity must be at least 1.")
                return redirect('product_detail', pk=pk)

            if product.stock < quantity:
                messages.error(request, f"Not enough stock for {product.name}. Available: {product.stock}")
                return redirect('product_detail', pk=pk)

            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

            if not created:
                cart_item.quantity = F('quantity') + quantity
            else:
                cart_item.quantity = quantity

            cart_item.save()
            messages.success(request, f"{quantity} x {product.name} added to cart!")
            return redirect('products')
    
    return render(request, 'product_detail.html', {'product': product, 'add_to_cart_form': add_to_cart_form})

@login_required
@never_cache
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.stock < 1:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect('products')

    item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        if product.stock < item.quantity + 1:
            messages.error(request, f"Cannot add more {product.name}. Only {product.stock} available in total.")
            return redirect('products')
        item.quantity = F('quantity') + 1
    item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('products')

@login_required
@never_cache
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'items': items})

@login_required
@never_cache
def update_cart_item(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, pk=pk, user=request.user)
        try:
            new_quantity = int(request.POST.get('quantity'))
            
            if new_quantity <= 0:
                item.delete()
                messages.info(request, f"{item.product.name} removed from cart.")
            else:
                if item.product.stock < new_quantity:
                    messages.error(request, f"Not enough stock for {item.product.name}. Only {item.product.stock} available.")
                    return redirect('cart')
                
                item.quantity = new_quantity
                item.save()
                messages.success(request, f"Quantity for {item.product.name} updated to {new_quantity}.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
    return redirect('cart')

@login_required
@never_cache
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    messages.info(request, f"{item.product.name} removed from cart.")
    return redirect('cart')

@login_required
@never_cache
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('products')

    order = Order.objects.create(user=request.user)
    total_order_price = 0

    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            messages.error(request, f"Not enough stock for {product.name}. Only {product.stock} available. Please adjust your cart.")
            order.delete()
            return redirect('cart')
        
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
        
        product.stock = F('stock') - item.quantity
        product.save()

        total_order_price += item.total_price()

    order.total_price = total_order_price
    order.save()

    cart_items.delete()

    messages.success(request, f"Checkout successful! Your order (ID: {order.id}) has been placed for ${order.total_price:.2f}.")
    return redirect('order_history')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def admin_products(request):
    """
    Displays a list of products for the logged-in user to manage.
    """
    products = Product.objects.filter(seller=request.user).order_by('name')
    return render(request, 'admin_products.html', {'products': products})

@login_required
def add_product(request):
    """
    Allows a user to add a new product.
    The new product will be associated with the current user.
    """
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_product = form.save(commit=False)
        new_product.seller = request.user
        new_product.save()
        messages.success(request, "Product added successfully!")
        return redirect('admin_products')
    return render(request, 'product_form.html', {'form': form, 'title': 'Add Product'})

@login_required
def edit_product(request, pk):
    """
    Allows a user to edit one of their products.
    Includes a security check to prevent editing products owned by others.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if product.seller != request.user:
        messages.error(request, "You do not have permission to edit this product.")
        return redirect('admin_products')

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, f"Product '{product.name}' updated successfully!")
        return redirect('admin_products')
    return render(request, 'product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def delete_product(request, pk):
    """
    Allows a user to delete one of their products.
    Includes a security check to prevent deleting products owned by others.
    """
    product = get_object_or_404(Product, pk=pk)
    
    if product.seller != request.user:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect('admin_products')

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' deleted successfully!")
        return redirect('admin_products')
    return render(request, 'confirm_delete.html', {'object': product})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})