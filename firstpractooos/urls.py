from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'firstpractooos'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/category/<int:category_id>/', views.catalog, name='catalog_by_category'),
    path('catalog/tags/<int:tag_id>/', views.catalog, name='tag'),
    path('product/<int:product_id>/', views.view_product, name='view_product'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('contacts/', views.contacts, name='contacts'),
    path('account/', views.account, name='account'),
    path('profile/', views.account, name='profile'),
    path('api/', views.api, name='api'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('categories/', views.category_list, name='category_list'),
    path('add_category/', views.add_category, name='add_category'),
    path('tags/', views.tag_list, name='tag_list'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('my-orders/', views.my_orders, name='my_orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)