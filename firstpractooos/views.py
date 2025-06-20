from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category, Tag, Order, OrderItem
from .forms import ProductForm, CategoryForm, TagForm
from cart.forms import CartAddProductForm 
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAdminUser


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'firstpractooos/my_orders.html', {'orders': orders})

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).filter(is_deleted=False)[:4]
    
    cart_product_form = CartAddProductForm()  
    
    context = {
        'product': product,
        'related_products': related_products,
        'cart_product_form': cart_product_form, 
    }
    return render(request, 'shablons/view_product.html', context)

def index(request):
    return render(request, 'shablons/index.html')

def catalog(request, category_id=None):
    products = Product.objects.filter(is_deleted=False)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    active_category = None
    active_tag = None
    
    if category_id:
        active_category = get_object_or_404(Category, id=category_id)  
        products = products.filter(category=active_category)
    
    tag_id = request.GET.get('tag_id')
    if tag_id:
        try:
            active_tag = get_object_or_404(Tag, id=int(tag_id))
            products = products.filter(tags=active_tag)
        except (ValueError, TypeError):
            pass
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'tags': tags,
        'active_category': active_category.id if active_category else None, 
        'active_tag': active_tag.id if active_tag else None,  
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    }
    return render(request, 'shablons/catalog.html', context)

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).filter(is_deleted=False)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shablons/view_product.html', context)

def cart(request):
    return render(request, 'shablons/cart.html')

def contacts(request):
    return render(request, 'shablons/contacts.html')

def account(request):
    return render(request, 'shablons/account.html')

def api(request):
    products = Product.objects.filter(is_deleted=False)
    context = {'items': products}
    return render(request, 'shablons/api.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('firstpractooos:api')
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'shablons/add_product.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('firstpractooos:catalog') 
        else:
            print(form.errors)
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'bike': product}
    return render(request, 'shablons/edit_products.html', context)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.is_deleted = True
        product.save()
        return redirect('firstpractooos:api')
    
    context = {'id': product_id}
    return render(request, 'shablons/delete_product.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shablons/category_list.html', context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('firstpractooos:category_list')
    else:
        form = CategoryForm()
    
    context = {'form': form}
    return render(request, 'shablons/add_category.html', context)

def tag_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'shablons/tag_list.html', context)