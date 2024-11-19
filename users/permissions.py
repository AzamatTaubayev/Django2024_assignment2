from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Student'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Teacher'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'