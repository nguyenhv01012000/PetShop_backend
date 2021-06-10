from rest_framework.permissions import BasePermission
from apps.external_apps.models.app import App

class AppPermission(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if isinstance(request.user, App):
            return request.user.active
        return False
