import re

def validate_minimum_length(field, field_name, min_length=3):
    if len(field) < min_length:
        return "{} should have a minimum length of {}".format(field_name, min_length)
    return None

def validate_passwords_match(password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match"
    return None

def validate_email_format(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format"
    return None

def validate_name_contains_only_letters(name, field_name):
    if not name.isalpha():
        return "{} should only contain letters".format(field_name)
    return None

def validate_create_user_request(request):
    errors = []
    validations = [
        validate_minimum_length(request.username, "Username"),
        validate_minimum_length(request.password, "Password"),
        validate_minimum_length(request.first_name, "First name"),
        validate_minimum_length(request.last_name, "Last name"),
        validate_passwords_match(request.password, request.confirm_password),
        validate_email_format(request.email),
        validate_name_contains_only_letters(request.first_name, "First name"),
        validate_name_contains_only_letters(request.last_name, "Last name")
    ]

    # Aggregate errors
    for validation in validations:
        if validation:
            errors.append(validation)

    return errors
