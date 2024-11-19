from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import PermissionDenied
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsStudent

class StudentProfileView(RetrieveUpdateAPIView):
    """
    Allows students to view and update their own profiles.
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_object(self):
        """
        Retrieve the student instance associated with the logged-in user.
        """
        try:
            return Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            raise PermissionDenied("You do not have a profile to access.")
