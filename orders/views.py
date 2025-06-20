from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import OrderCreateForm
from firstpractooos.models import Order, OrderItem
from django.contrib import messages
from django.utils import timezone
import random
import string

@login_required
def order_create(request):
    cart = Cart(request)
    
    if not cart:
        messages.error(request, "Ваша корзина пуста")
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
                
                order = Order.objects.create(
                    order_number=order_number,
                    customer_name=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
                    customer_phone=form.cleaned_data['phone'],
                    delivery_address=(
                        f"Город: {form.cleaned_data['city']}, "
                        f"Адрес: {form.cleaned_data['address']}, "
                        f"Индекс: {form.cleaned_data['postal_code']}, "
                        f"Email: {form.cleaned_data['email']}, "
                        f"Комментарий: {form.cleaned_data['comments']}"
                    )
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        discount_per_unit=0.00 
                    )
                
                cart.clear()
                
                return render(request, 'orders/order_created.html', {
                    'order': order,
                    'customer_name': f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data['phone'],
                    'address': form.cleaned_data['address'],
                    'city': form.cleaned_data['city'],
                    'postal_code': form.cleaned_data['postal_code'],
                    'comments': form.cleaned_data['comments'],
                    'total_price': sum(item['product'].price * item['quantity'] for item in cart)
                })
                
            except Exception as e:
                messages.error(request, f"Ошибка при оформлении заказа: {str(e)}")
                return redirect('orders:order_create')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form
    })