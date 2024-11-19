# attendance/views.py
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacher

class AttendanceMarkView(CreateAPIView):
    """Mark attendance for a student."""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        """
        Ensure the teacher is the instructor of the course and the student is enrolled.
        """
        course = serializer.validated_data['course']
        student = serializer.validated_data['student']

        # Check if the logged-in user is the instructor for the course
        if course.instructor != self.request.user:
            raise PermissionDenied("You are not the instructor for this course.")

        # Check if the student is enrolled in the course
        if not course.students.filter(id=student.id).exists():
            raise PermissionDenied("This student is not enrolled in the course.")

        # Save the attendance record
        serializer.save()
