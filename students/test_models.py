from django.test import TestCase
from users.models import CustomUser
from students.models import Student


class StudentModelTests(TestCase):

    def setUp(self):
        """Set up a user and student instance for testing."""
        self.user = CustomUser.objects.create_user(
            username="teststudent",
            password="testpassword123",
            email="teststudent@example.com",
            role="Student"
        )
        self.student = Student.objects.create(user=self.user)

    def test_student_creation(self):
        """Test student profile creation."""
        self.assertEqual(self.student.user.username, "teststudent")
        self.assertIsInstance(self.student, Student)

    def test_student_update(self):
        """Test updating a student's profile."""
        self.student.bio = "Updated bio"
        self.student.save()
        self.student.refresh_from_db()
        self.assertEqual(self.student.bio, "Updated bio")

    def test_student_deletion(self):
        """Test deleting a student profile."""
        student_count = Student.objects.count()
        self.student.delete()
        self.assertEqual(Student.objects.count(), student_count - 1)
