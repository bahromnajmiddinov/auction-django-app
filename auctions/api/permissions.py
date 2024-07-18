from rest_framework import permissions


class BaseAuctionPermission(permissions.BasePermission):
    permission_field = None

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if self.permission_field is None:
            raise NotImplementedError("Subclasses must define 'permission_field'")

        user_perm = obj.auctionuserpermission_set.filter(user=request.user).first()
        if user_perm is None:
            return False
        return getattr(user_perm, self.permission_field, False)
        

class CanDeleteAuction(BaseAuctionPermission):
    permission_field = 'can_delete'


class CanEditAuction(BaseAuctionPermission):
    permission_field = 'can_edit'


class CanAddAdminToAuction(BaseAuctionPermission):
    permission_field = 'can_add_admin'


class IsAdminOfAuction(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.permissions.all()
    