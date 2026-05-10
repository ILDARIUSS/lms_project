from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = 'Доступ разрешен только модератору.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()


class IsNotModerator(BasePermission):
    message = 'Модератору запрещено выполнять это действие.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    message = 'Вы можете работать только со своими объектами.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModeratorOrOwner(BasePermission):
    message = 'Доступ разрешен только владельцу объекта или модератору.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_moderator = request.user.groups.filter(name='moderators').exists()
        return is_moderator or obj.owner == request.user