from rest_framework import permissions

class CustomModelPermissions(permissions.DjangoModelPermissions):
    
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает полный доступ только админам, остальным - только чтение
    """
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта или админу
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
            
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
    
class IsAdminOrSeller(permissions.BasePermission):
    """
    Разрешает доступ только администраторам и продавцам.
    Администратор - это пользователь с is_staff=True.
    Продавец - это пользователь в группе "Продавцы".
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True
        
        return request.user.groups.filter(name='Продавцы').exists()

class IsAdminOnly(permissions.BasePermission):
    """
    Разрешает доступ только администраторам (is_staff=True)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта или администратору
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
            
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False