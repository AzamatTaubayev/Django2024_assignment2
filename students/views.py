from django.core.cache import cache
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import PermissionDenied
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsStudent

class StudentProfileView(RetrieveUpdateAPIView):

    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'email']


def get_object(self):
    cache_key = f'student_profile_{self.request.user.id}'
    student_profile = cache.get(cache_key)

    if not student_profile:
        try:
            student_profile = Student.objects.get(user=self.request.user)
            cache.set(cache_key, student_profile, timeout=300)
        except Student.DoesNotExist:
            raise PermissionDenied("You do not have a profile to access.")

    return student_profile

def perform_update(self, serializer):
        cache_key = f'student_profile_{self.request.user.id}'
        cache.delete(cache_key)

        serializer.save()