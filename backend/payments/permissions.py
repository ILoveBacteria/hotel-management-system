from rest_framework import permissions


class IsBillOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.reserve.user == request.user