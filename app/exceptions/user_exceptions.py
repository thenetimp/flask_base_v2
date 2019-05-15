
# Any specific exceptions that are required for the user class
class UserExistsException(BaseException):
  error = { 'status': 'error', 'code': 'error_user_exists', 'message': 'A user with the email address exists', 'origin_message': None }


# Any specific exceptions that are required for the user class
class UserUnknownException(BaseException):
  error = { 'status': 'error', 'code': 'error_user_unknown', 'message': 'A user with the email address does not exist', 'origin_message': None }
    