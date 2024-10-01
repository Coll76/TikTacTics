from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit or delete.
    Regular users can only read the data.
    """

    def has_permission(self, request, view):
        # Allow read-only access to any request
        if request.method in permissions.SAFE_METHODS:

            return True
        # Full access for admins only
        return request.user and request.user.is_staff
