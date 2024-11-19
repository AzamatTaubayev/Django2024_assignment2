# attendance/urls.py
from django.urls import path
from .views import AttendanceMarkView

urlpatterns = [
    path('attendance/mark/', AttendanceMarkView.as_view(), name='attendance-mark'),
]
