from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Предоставляет доступ автору, другим только для чтения."""

    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or object.author == request.user
        )
