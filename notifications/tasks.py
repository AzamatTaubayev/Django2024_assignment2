# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from students.models import Student  # Assuming you have a Student model

@shared_task
def send_attendance_reminder():
    """Send a daily reminder to students to mark their attendance."""
    today = timezone.now().date()
    students = Student.objects.all()

    for student in students:
        send_mail(
            'Attendance Reminder',
            f'Hi {student.name}, please remember to mark your attendance today, {today}.',
            'from@example.com',  # Replace with your email
            [student.user.email],
            fail_silently=False,
        )
    return 'Attendance reminder sent to all students.'

@shared_task
def notify_grade_update(student_id, course_name, grade):
    """Notify students when their grade is updated."""
    student = Student.objects.get(id=student_id)
    send_mail(
        'Grade Update',
        f'Hi {student.name}, your grade for {course_name} has been updated to {grade}.',
        'from@example.com',  # Replace with your email
        [student.user.email],
        fail_silently=False,
    )
    return 'Grade update notification sent.'
@shared_task
def send_weekly_performance_report():
    """Send weekly email updates summarizing each student’s performance."""
    students = Student.objects.all()

    for student in students:
        # Prepare the performance report for the student
        report = f'Weekly performance summary for {student.name}...'

        send_mail(
            'Weekly Performance Report',
            report,
            'from@example.com',  # Replace with your email
            [student.user.email],
            fail_silently=False,
        )
    return 'Weekly performance report sent to all students.'