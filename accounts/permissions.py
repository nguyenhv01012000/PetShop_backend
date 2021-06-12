from rest_framework.permissions import BasePermission


class PracticeProgramPermission(BasePermission):
    def has_permission(self, request, view):
        return True