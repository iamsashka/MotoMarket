# serializers.py
from rest_framework import serializers
from firstpractooos.models import Category, Tag, Product, ProductTag, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'description']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name', 'description']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'description', 'price', 'image',
            'created_at', 'updated_at', 'is_deleted', 'category', 'tags'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'product', 'tag', 'created_at']
        read_only_fields = ['id', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'discount_per_unit', 'total_price']
        read_only_fields = ['id', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'created_at',
            'customer_name', 'customer_phone',
            'delivery_address', 'items', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'order_number', 'user']