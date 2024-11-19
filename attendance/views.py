# attendance/views.py
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from users.permissions import IsTeacherOrAdmin
from .models import Attendance
from .serializers import AttendanceSerializer
import logging


logger = logging.getLogger('SMS')

class AttendanceMarkView(CreateAPIView):
    """Mark attendance for a student."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        student = serializer.validated_data['student']

        if course.instructor != self.request.user:
            raise PermissionDenied("You are not the instructor for this course.")

        if not course.students.filter(id=student.id).exists():
            raise PermissionDenied("This student is not enrolled in the course.")

        serializer.save()

        logger.info(f"Attendance marked: Course: {course.name}, Student: {student.name}, Teacher: {self.request.user.username}")

