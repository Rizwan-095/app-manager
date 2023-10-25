from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .validators import custom_password_validator, is_valid_email


def validate_registration_data(view_func):
    def _wrapped_view(request):
        data = request.data

        if 'first_name' not in data:
            return Response({"error": "First name is required."}, status=status.HTTP_400_BAD_REQUEST)
        if 'email' not in data:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in data:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        if 'confirm_password' not in data:
            return Response({"error": "confirm_password is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_email(data['email']):
            return Response({"error": "invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        is_password_valid = custom_password_validator(data['password'])
        if is_password_valid['error'] == True:
            return Response({'error': is_password_valid['message']}, status=status.HTTP_400_BAD_REQUEST)

        if data['password'] != data['confirm_password']:
            return Response({"error": "passwords did not match"}, status=status.HTTP_400_BAD_REQUEST)

        if Account.objects.filter(email=data['email']).exists():
            return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

        return view_func(request)

    return _wrapped_view
