from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if request.user.role == "admin" and is_authenticated:
            return is_authenticated
        return False
    
class RestaurantPermission(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if is_authenticated and request.user.role == "restaurant":
            return is_authenticated
        return False