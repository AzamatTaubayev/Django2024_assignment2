# grades/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView

from users.permissions import IsTeacherOrAdmin
from .models import Grade
from rest_framework.exceptions import PermissionDenied

from .serializers import GradeSerializer
import logging

logger = logging.getLogger('SMS')

class GradeCreateView(CreateAPIView):
    """Add grade for a student in a course (teachers/admin only)."""
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.instructor != self.request.user and self.request.user.role != 'Admin':
            raise PermissionDenied("You are not the instructor for this course.")
        serializer.save(teacher=self.request.user)
        logger.info(f"Grade added: Course: {course.name}, Student: {serializer.validated_data['student'].name}, Grade: {serializer.validated_data['grade']}, Teacher: {self.request.user.username}")


class GradeUpdateView(UpdateAPIView):
    """Edit grade for a student (teachers/admin only)."""
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def perform_update(self, serializer):
        course = serializer.validated_data['course']
        if course.instructor != self.request.user and self.request.user.role != 'Admin':
            raise PermissionDenied("You are not the instructor for this course.")
        serializer.save()
        logger.info(f"Grade updated: Course: {course.name}, Student: {serializer.validated_data['student'].name}, New Grade: {serializer.validated_data['grade']}, Teacher: {self.request.user.username}")


class GradeListView(ListAPIView):
    """List grades for a student (any authenticated user)."""
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter grades for the logged-in user
        if self.request.user.role == 'Student':
            return self.queryset.filter(student=self.request.user)
        return self.queryset
