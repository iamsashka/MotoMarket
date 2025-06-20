from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductTagViewSet,
    OrderViewSet,
    OrderItemViewSet
)

router = routers.SimpleRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-tags', ProductTagViewSet, basename='product-tag')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

def get_dynamic_urls():
    """Функция для получения динамических URL"""
    return router.urls

