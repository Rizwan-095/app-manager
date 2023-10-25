import re


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


def custom_password_validator(password):
    # Check for at least 8 characters
    if len(password) < 8:
        return {'error': True, 'message': 'password length must be equal or greater than 8 characters.'}

    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return {'error': True, 'message': 'password must contain uppercase letters as well.'}

    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return {'error': True, 'message': 'password must contain digits as well.'}

    # Check for at least one special character
    if not any(not char.isalnum() for char in password):
        return {'error': True, 'message': 'password must be combination of alphanumeric, special & uppercas characters.'}
    return {'error': False, 'message': ''}
