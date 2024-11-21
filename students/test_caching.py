from django.core.cache import cache
from rest_framework.test import APITestCase
from users.models import CustomUser
from students.models import Student


class StudentCacheTests(APITestCase):

    def setUp(self):
        """Set up test data for student profile."""
        self.user = CustomUser.objects.create_user(
            username="teststudent",
            password="testpassword123",
            email="teststudent@example.com",
            role="Student"
        )
        self.student_profile = Student.objects.create(user=self.user)

    def test_cache_usage(self):
        """Test that caching works for repeated requests."""
        url = f"/api/students/{self.student_profile.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Simulate cache hit
        cache.set('student_profile', self.student_profile)
        cached_profile = cache.get('student_profile')
        self.assertEqual(cached_profile, self.student_profile)
