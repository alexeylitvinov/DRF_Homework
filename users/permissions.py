from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Устанавливает права для модераторов.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsUser(permissions.BasePermission):
    """
    Устанавливает права для пользователя.
    """
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False

