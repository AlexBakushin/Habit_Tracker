from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Пермишен проверяет, является ли пользователь владельцем привычки
    """

    # def has_permission(self, request, view):
    #     return request.user == view.get_object()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsModer(BasePermission):
    """
    Пермишен проверяет, является ли пользователь модератором
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderator').exists()


class IsOwnerOrModerator(BasePermission):
    """
    Пермишен проверяет, является ли пользователь владельцем привычки или модератором
    """
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderator').exists() or request.user.is_superuser:
            return True

        return obj.user == request.user
