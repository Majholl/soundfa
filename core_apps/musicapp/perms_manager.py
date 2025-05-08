from rest_framework.permissions import BasePermission



class AllowAuthenticatedAndAdminsAndSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated: 
            return False
        return bool(user.is_authenticated and (user.usertype == 'admin' or user.is_superuser))
    
    
    
class Is_superadmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)