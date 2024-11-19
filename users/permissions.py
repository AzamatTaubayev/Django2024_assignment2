from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Student'

class IsTeacherOrAdmin(BasePermission):
    """
    Allows access only to teachers or admins.
    """
    def has_permission(self, request, view):
        return request.user.role in ['Teacher', 'Admin']