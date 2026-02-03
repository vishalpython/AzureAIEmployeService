from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # Only allow authenticated users (default), or add custom logic here
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        print(obj.user,request.user,"yyyyyyyyyyyyyyyyyyyyyyy")
        if request.method in SAFE_METHODS:
            return True
        
        return obj.user == request.user
    
