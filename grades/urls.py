from django.urls import path
from .views import GradeCreateView, GradeUpdateView, GradeListView

urlpatterns = [
    path('', GradeListView.as_view(), name='grade-list'),
    path('create/', GradeCreateView.as_view(), name='grade-create'),
    path('<int:pk>/edit/', GradeUpdateView.as_view(), name='grade-update'),
]
