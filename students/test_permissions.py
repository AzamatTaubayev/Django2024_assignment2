from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from students.models import Student

class StudentPermissionTests(APITestCase):

    def setUp(self):
        """Set up test data for permissions."""
        self.teacher = CustomUser.objects.create_user(
            username="testteacher",
            password="testpassword123",
            email="testteacher@example.com",
            role="Teacher"
        )
        self.student = CustomUser.objects.create_user(
            username="teststudent",
            password="testpassword123",
            email="teststudent@example.com",
            role="Student"
        )
        self.student_profile = Student.objects.create(user=self.student)

    def test_student_access(self):
        """Test that students cannot access each other's profiles."""
        self.client.login(username="teststudent", password="testpassword123")
        response = self.client.get(f"/api/students/{self.student_profile.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now, check if a different student tries to access the profile.
        self.client.logout()
        self.client.login(username="testteacher", password="testpassword123")
        response = self.client.get(f"/api/students/{self.student_profile.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
