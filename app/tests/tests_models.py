from flask_testing import TestCase
from app import create_app
from app.models import User
from app.models.user_model import db as user_db

class ModelTest(TestCase):

  # Create the application
  def create_app(self):
    print("Creating the flask app")
    return create_app("test")

  def test_user_model(self):

    # Define variables for tests
    first_name = 'John'
    last_name = 'Doe'
    email_address = "test@testuser.com"
    email_address_two = "testtwo@testuser.com"
    password = 'testing123456'
    password_two = '123456testing'

    # Check if the user already exists
    user = User.get_user_by_email_address(email_address)

    # Make sure the user doesn't exist
    self.assertIsNone(user)

    # Create the users
    user = User.create_user(first_name, last_name, email_address, password)

    # Make sure the user doesn't exist
    self.assertIsNotNone(user)

    # Check if the user exists in the database and compare it to
    # the user that we received before the last test.
    user_two = User.get_user_by_email_address(email_address)
    self.assertEqual(user, user_two)

    # Check that the password check works
    self.assertTrue(user.check_password(password))

    # Set a new password
    user.update_password(password_two)

    # Make sure the passwords are no longer the same
    self.assertFalse(user.check_password(password))
 
    # Check that the password check works
    self.assertTrue(user.check_password(password_two))

    # Generate a reset token for non existant user
    user_three = User.generate_password_reset_token(email_address_two)

    # Make sure the user doesn't exist
    self.assertIsNone(user_three)

    # Generate a reset token for non existant user
    reset_token = User.generate_password_reset_token(email_address)

    # Make sure the user doesn't exist
    self.assertIsNotNone(reset_token)

    # Clear the reset token.
    user.clear_password_token()

    # Make sure the user doesn't exist
    self.assertEqual(user.password_reset_token, '')