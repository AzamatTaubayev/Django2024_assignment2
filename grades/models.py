# grades/models.py
from django.db import models
from students.models import Student
from courses.models import Course

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)  # e.g., A+, B, etc.
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(
        'users.CustomUser', on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'Teacher'}
    )

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.grade}"
