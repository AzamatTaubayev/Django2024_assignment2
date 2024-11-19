# grades/serializers.py
from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date', 'teacher']
        read_only_fields = ['id', 'date', 'teacher']
