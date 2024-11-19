# users/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import CustomUser


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Get role from request data, default to 'Student' if not provided
        role = request.data.get('role', 'Student')

        # Validate role
        if role not in ['Student', 'Teacher', 'Admin']:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Set the role
        user.role = role
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Return user data along with tokens
        return Response({
            'user': UserSerializer(user).data,
            'access': str(access_token),
            'refresh': str(refresh),
        })
