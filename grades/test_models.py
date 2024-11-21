from django.test import TestCase
from users.models import CustomUser
from students.models import Student
from grades.models import Grade
from courses.models import Course


class GradeModelTests(TestCase):

    def setUp(self):
        """Set up user, student, course, and grade instances for testing."""
        self.user = CustomUser.objects.create_user(
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
        self.course = Course.objects.create(name="Test Course", instructor=self.user)
        self.student_profile = Student.objects.create(user=self.student)
        self.grade = Grade.objects.create(student=self.student_profile, course=self.course, grade=85)

    def test_grade_creation(self):
        """Test the creation of a grade for a student."""
        self.assertEqual(self.grade.grade, 85)
        self.assertEqual(self.grade.student.user.username, "teststudent")

    def test_grade_update(self):
        """Test that grades can be updated."""
        self.grade.grade = 90
        self.grade.save()
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.grade, 90)

    def test_grade_deletion(self):
        """Test that grades can be deleted."""
        grade_count = Grade.objects.count()
        self.grade.delete()
        self.assertEqual(Grade.objects.count(), grade_count - 1)
