from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    message = "Access denied! This is not your movie collection."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user