from rest_framework import permissions


class UpdateOwnContent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user.id == request.user.id


class AdminOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser == True:
            return True
