from django.urls import path
from .views import GradeCreateView, GradeUpdateView, GradeListView

urlpatterns = [
    path('grades/', GradeListView.as_view(), name='grade-list'),
    path('grades/create/', GradeCreateView.as_view(), name='grade-create'),
    path('grades/<int:pk>/edit/', GradeUpdateView.as_view(), name='grade-update'),
]
