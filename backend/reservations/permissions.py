from rest_framework.permissions import IsAuthenticated


class IsReserveOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class IsCancelledReserveOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.reserve.user == request.user