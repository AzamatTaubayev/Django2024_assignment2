# courses/urls.py
from django.urls import path
from .views import CourseListView, CourseCreateView, CourseUpdateView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course-update'),
]
