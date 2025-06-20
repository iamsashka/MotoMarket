from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import (
    CategorySerializer,
    TagSerializer,
    ProductSerializer,
    ProductTagSerializer,
    OrderSerializer,
    OrderItemSerializer
)
from firstpractooos.models import (
    Category,
    Tag,
    Product,
    ProductTag,
    Order,
    OrderItem
)
from .permissions import IsAdminOrSeller, IsAdminOnly, IsOwnerOrAdmin

# Apply login_required to all API views
class LoginRequiredViewSet(viewsets.ModelViewSet):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CategoryViewSet(LoginRequiredViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

class TagViewSet(LoginRequiredViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

class ProductViewSet(LoginRequiredViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ProductTagViewSet(LoginRequiredViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

class OrderViewSet(LoginRequiredViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemViewSet(LoginRequiredViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]