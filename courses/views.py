# courses/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from .models import Course
from users.permissions import IsTeacher, IsAdmin
from rest_framework.exceptions import PermissionDenied

from .serializers import CourseSerializer


class CourseListView(ListAPIView):
    """View all courses."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]  # Everyone can view courses

class CourseCreateView(CreateAPIView):
    """Add a new course (teachers/admin only)."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsAdmin]

    def perform_create(self, serializer):
        # Ensure only teachers or admin can create a course
        if self.request.user.role not in ['Teacher', 'Admin']:
            raise PermissionDenied("You do not have permission to create a course.")
        serializer.save(instructor=self.request.user)

class CourseUpdateView(UpdateAPIView):
    """Edit course details (teachers/admin only)."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher, IsAdmin]

    def perform_update(self, serializer):
        # Ensure only the instructor or admin can update the course
        if self.get_object().instructor != self.request.user and self.request.user.role != 'Admin':
            raise PermissionDenied("You are not allowed to edit this course.")
        serializer.save()
