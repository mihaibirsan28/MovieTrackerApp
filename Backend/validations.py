import re

from request_models import CreateUserRequest


def validate_create_user_request(request: CreateUserRequest):
    errors = []

    # Minimum length check for all fields
    min_length = 3  # Define your minimum length
    if len(request.username) < min_length:
        errors.append("Username should have a minimum length of {}".format(min_length))
    if len(request.password) < min_length:
        errors.append("Password should have a minimum length of {}".format(min_length))
    if len(request.first_name) < min_length:
        errors.append("First name should have a minimum length of {}".format(min_length))
    if len(request.last_name) < min_length:
        errors.append("Last name should have a minimum length of {}".format(min_length))

    # Passwords match check
    if request.password != request.confirm_password:
        errors.append("Passwords do not match")

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", request.email):
        errors.append("Invalid email format")

    # Names only contain letters check
    if not request.first_name.isalpha():
        errors.append("First name should only contain letters")
    if not request.last_name.isalpha():
        errors.append("Last name should only contain letters")
    return errors
