from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        owner_field = getattr(view, "owner_field", "author")
        owner = obj if owner_field == "self" else getattr(obj, owner_field, None)
        return owner == request.user
