from django.db import models
from django.utils import timezone

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'category'  
    
    def __str__(self):
        return self.category_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'tag'  
    
    def __str__(self):
        return self.tag_name

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, through='ProductTag')
    
    class Meta:
        db_table = 'product' 
    
    def __str__(self):
        return self.product_name

class ProductTag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE,
        related_name='product_tags'
    )
    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
        related_name='tagged_products'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_tag'
        unique_together = ('product', 'tag')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product} - {self.tag}"

class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()
    customer_phone = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=255)
    
    
    class Meta:
        db_table = 'order_moto'  
    
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    discount_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'order_item'  
        unique_together = ('order', 'product')
    
    @property
    def total_price(self):
        return (self.product.price - self.discount_per_unit) * self.quantity