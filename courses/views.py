# courses/views.py
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .models import Course, Enrollment
from users.permissions import IsTeacherOrAdmin, IsStudent
from rest_framework.exceptions import PermissionDenied
import logging

from .serializers import CourseSerializer, EnrollmentSerializer

logger = logging.getLogger('SMS')

class CourseListView(ListAPIView):
    """View all courses."""
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'instructor__username']  # Filter by course name or instructor
    search_fields = ['name', 'description']  # Search by name or description
    ordering_fields = ['name', 'id']

    def get_queryset(self):
        """
        Cache the queryset of courses based on the filters.
        """
        # Generate a cache key based on the filters and query parameters
        cache_key = f'course_list_{self.request.user.id}_{self.request.GET.get("instructor__username", "")}_{self.request.GET.get("name", "")}'

        # Try to get the cached data
        cached_courses = cache.get(cache_key)
        if cached_courses:
            return cached_courses  # Return the cached result if available

        # If cache is not available, query the database
        queryset = Course.objects.all()

        # Apply filters
        if 'instructor__username' in self.request.GET:
            queryset = queryset.filter(instructor__username=self.request.GET['instructor__username'])
        if 'name' in self.request.GET:
            queryset = queryset.filter(name__icontains=self.request.GET['name'])

        # Cache the result for 1 hour (you can adjust the time)
        cache.set(cache_key, queryset, timeout=3600)  # Cache for 1 hour

        return queryset
class CourseCreateView(CreateAPIView):
    """Add a new course (teachers/admin only)."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def perform_create(self, serializer):
        # Ensure only teachers or admin can create a course
        if self.request.user.role not in ['Teacher', 'Admin']:
            raise PermissionDenied("You do not have permission to create a course.")
        serializer.save(instructor=self.request.user)

class CourseUpdateView(UpdateAPIView):
    """Edit course details (teachers/admin only)."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def perform_update(self, serializer):
        # Ensure only the instructor or admin can update the course
        if self.get_object().instructor != self.request.user and self.request.user.role != 'Admin':
            raise PermissionDenied("You are not allowed to edit this course.")
        course = serializer.save()

        cache_key = f'course_list_{self.request.user.id}_{self.request.GET.get("instructor__username", "")}_{self.request.GET.get("name", "")}'
        cache.delete(cache_key)

        return course

class EnrollmentCreateView(CreateAPIView):
    """
    Allow students to enroll in a course.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        # Ensure the student is enrolling themselves
        student = serializer.validated_data['student']
        if student.user != self.request.user:
            raise PermissionDenied("You can only enroll yourself in a course.")
        logger.info(f"Student {student.user.username} enrolled in course {serializer.validated_data['course'].name}")
        serializer.save()


class EnrollmentListView(ListAPIView):
    """
    View all enrollments for a specific course (teachers/admin only).
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student__name', 'course__name']  # Filter by student or course
    search_fields = ['student__name', 'course__name']  # Search by student or course
    ordering_fields = ['enrollment_date']

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Enrollment.objects.filter(course_id=course_id)


class EnrollmentDeleteView(DestroyAPIView):
    """
    Allow teachers/admins to remove a student from a course.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def perform_destroy(self, instance):
        # Only the instructor or an admin can remove a student
        if instance.course.instructor != self.request.user and self.request.user.role != 'Admin':
            raise PermissionDenied("You are not allowed to remove a student from this course.")
        instance.delete()