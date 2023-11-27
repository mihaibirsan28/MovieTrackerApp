import unittest
from validations import (
    validate_minimum_length,
    validate_passwords_match,
    validate_email_format,
    validate_name_contains_only_letters, validate_create_user_request
)


class MockRequest:
    def __init__(self, username, password, confirm_password, first_name, last_name, email):
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
class TestUserValidationFunctions(unittest.TestCase):

    def test_validate_minimum_length(self):
        self.assertIsNone(validate_minimum_length("username", "Username", 3))
        self.assertEqual(
            validate_minimum_length("us", "Username", 3),
            "Username should have a minimum length of 3"
        )

    def test_validate_passwords_match(self):
        self.assertIsNone(validate_passwords_match("password123", "password123"))
        self.assertEqual(
            validate_passwords_match("password123", "pass1234"),
            "Passwords do not match"
        )

    def test_validate_email_format(self):
        self.assertIsNone(validate_email_format("mihaitestare@example.com"))
        self.assertEqual(
            validate_email_format("mihaitestare.com"),
            "Invalid email format"
        )

    def test_validate_name_contains_only_letters(self):
        self.assertIsNone(validate_name_contains_only_letters("Robero", "First name"))
        self.assertEqual(
            validate_name_contains_only_letters("Robero3", "First name"),
            "First name should only contain letters"
        )

    def test_all_valid_inputs(self):
        request = MockRequest("username", "password123", "password123", "Cristi", "Che", "mihaitestare@example.com")
        errors = validate_create_user_request(request)
        self.assertEqual(len(errors), 0)

    def test_invalid_inputs(self):
        request = MockRequest("us", "pw", "pwx", "Cristi6", "Test!", "testulina.com")
        errors = validate_create_user_request(request)
        self.assertEqual(len(errors), 6)
        self.assertIn("Username should have a minimum length of 3", errors)
        self.assertIn("Password should have a minimum length of 3", errors)
        self.assertIn("Passwords do not match", errors)
        self.assertIn("First name should only contain letters", errors)
        self.assertIn("Last name should only contain letters", errors)
        self.assertIn("Invalid email format", errors)

if __name__ == '__main__':
    unittest.main()
