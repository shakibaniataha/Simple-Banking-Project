from rest_framework import permissions


class IsAuthenticatedCustomer(permissions.BasePermission):
    message = 'You must be an authenticated customer'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'customer'))


class IsAuthenticatedClerk(permissions.BasePermission):
    message = 'You must be an authenticated clerk'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'clerk'))


class IsAuthenticatedAdmin(permissions.BasePermission):
    message = 'You must be an authenticated admin'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
