from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Предоставляет доступ админу, другим только для чтения."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)


class AuthorOrReadOnly(permissions.BasePermission):
    """Предоставляет доступ автору, другим только для чтения."""

    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or object.author == request.user
        )
