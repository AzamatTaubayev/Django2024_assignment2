from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser


class GradeViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')  # Authenticate user

    def test_create_grade(self):
        response = self.client.post('/api/grades/', data={'grade': 90, 'course': self.course.id, 'student': self.student.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
