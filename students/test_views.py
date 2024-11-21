from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from students.models import Student

class StudentProfileViewTests(APITestCase):

    def setUp(self):
        """Set up test data for student profile."""
        self.user = CustomUser.objects.create_user(
            username="teststudent",
            password="testpassword123",
            email="teststudent@example.com",
            role="Student"
        )
        self.client.login(username="teststudent", password="testpassword123")
        self.student_profile = Student.objects.create(user=self.user)

        # Get the URL for the student profile view
        self.url_create = reverse('student-profile')  # Adjust the reverse name based on your `urls.py`
        self.url_update = reverse('student-profile')  # Same as create, but we'll use the `id` to update
        self.url_delete = reverse('student-profile')  # Same as create, we'll pass `id` for delete

    def test_create_student_profile(self):
        """Test that a student profile can be created."""
        data = {
            "bio": "This is a test bio"
        }
        response = self.client.post(self.url_create, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['bio'], "This is a test bio")

    def test_update_student_profile(self):
        """Test that a student profile can be updated."""
        url = f"/api/students/{self.student_profile.id}/"
        data = {"bio": "Updated bio"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], "Updated bio")

    def test_delete_student_profile(self):
        """Test that a student profile can be deleted."""
        url = f"/api/students/{self.student_profile.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
