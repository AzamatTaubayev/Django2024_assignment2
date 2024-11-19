# courses/urls.py
from django.urls import path
from .views import CourseListView, CourseCreateView, CourseUpdateView, EnrollmentCreateView, EnrollmentListView, \
    EnrollmentDeleteView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course-update'),

    path('courses/enroll/', EnrollmentCreateView.as_view(), name='enroll-student'),
    path('courses/<int:course_id>/enrollments/', EnrollmentListView.as_view(), name='list-enrollments'),
    path('enrollments/<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='delete-enrollment'),
]
