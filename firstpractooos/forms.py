# forms.py
from django import forms
from .models import Product, Category, Tag, Order, OrderItem 


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name', 
            'description', 
            'price', 
            'image', 
            'category', 
            'tags',
            'is_deleted'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_deleted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'product_name': 'Название мотоцикла',
            'description': 'Описание',
            'price': 'Цена (руб)',
            'image': 'Изображение',
            'category': 'Категория',
            'tags': 'Теги',
            'is_deleted': 'Снят с продажи',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['tags'].queryset = Tag.objects.all()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название категории'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Описание категории'
            }),
        }
        labels = {
            'category_name': 'Название категории',
            'description': 'Описание',
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_name', 'description']
        widgets = {
            'tag_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название тега'
            }),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Описание тега'
            }),
        }
        labels = {
            'tag_name': 'Название тега',
            'description': 'Описание',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'order_number',
            'delivery_address', 
            'customer_phone', 
            'customer_name'
        ]
        widgets = {
            'order_number': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'delivery_address': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'order_number': 'Номер заказа',
            'delivery_address': 'Адрес доставки',
            'customer_phone': 'Телефон клиента',
            'customer_name': 'ФИО клиента',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            last_order = Order.objects.order_by('-id').first()
            last_id = last_order.id if last_order else 0
            self.initial['order_number'] = f'ORD-{last_id + 1:04d}'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'discount_per_unit']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'discount_per_unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.00'
            }),
        }
        labels = {
            'product': 'Мотоцикл',
            'quantity': 'Количество',
            'discount_per_unit': 'Скидка на единицу (руб)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_deleted=False)


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию или описанию'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        required=False,
        label='Минимальная цена',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        label='Максимальная цена',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
        })
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Теги',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )