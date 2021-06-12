from rest_framework.permissions import BasePermission, DjangoModelPermissions

from apps.users.models.staff import Staff
from apps.users.models.user import User


class IsStaffPermission(BasePermission):
    message = "Action is not allowed."

    def has_permission(self, request, view):
        return isinstance(request.user, Staff)


class IsUserPermission(BasePermission):
    message = "Action is not allowed."

    def has_permission(self, request, view):
        return isinstance(request.user, User)


class RolePermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
