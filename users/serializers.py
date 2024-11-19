from django.contrib.auth import get_user_model
from rest_framework import serializers

from students.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Handle the role field, default to 'Student' if not provided
        role = validated_data.get('role', 'Student')
        # Create the user using the model's create_user method
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )

        if role == 'Student':
            Student.objects.create(user=user, name=user.username, email=user.email)

        return user
