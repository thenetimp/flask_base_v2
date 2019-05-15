import uuid
from datetime import datetime, timedelta
from app import bcrypt, db
from app.exceptions.user_exceptions import *
from sqlalchemy import Table, Column, Integer, Numeric, String, Boolean, DateTime

class User(db.Model):

  __tablename__ = 'user'

  user_id = Column(Integer(), primary_key=True)
  email_address = Column(String(255), nullable=False, unique=True)
  password = Column(String(25), nullable=False)
  first_name = Column(String(25), nullable=False)
  last_name = Column(String(25), nullable=False)
  password_reset_token = Column(String(255), default='', nullable=False)
  created_on = Column(DateTime(), default=datetime.now)
  updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


  # Initialize model
  def __init__(self, email_address=None, first_name=None, last_name=None, password=None):
    self.email_address = email_address
    self.first_name = first_name
    self.last_name = last_name
    self.encrypt_password(password)


  # Check the hashed password against the plaintext password.
  def check_password(self, password):
    return bcrypt.check_password_hash(self.password, password)


  # Encrypt a plain text password
  def encrypt_password(self, password):
    self.password = bcrypt.generate_password_hash(password)


  # Clear the password reset token to an empty string
  def clear_password_token(self):
    self.password_reset_token=""
    self.password_reset_token_expire = (datetime.now() - timedelta(days=2))
    db.session.add(self)
    db.session.commit()


  # Update the password
  def update_password(self, password):
    self.encrypt_password(password)
    db.session.add(self)
    db.session.commit()


  # Create the user static function
  @staticmethod
  def create_user(first_name, last_name, email_address, password):

    # Try to get existing user
    user = User.get_user_by_email_address(email_address)

    # If the user exists raise an exception
    if user is not None:
      raise UserExistsException

    # Create a user record
    user = User(first_name=first_name, last_name=last_name, email_address=email_address, password=password)
    db.session.add(user)
    db.session.commit()
    return user


  # Get user by email address static function
  @staticmethod
  def get_user_by_email_address(email_address):
    user = User.query.filter_by(email_address=email_address).first()
    return user


  # Get password reset token by email address static function
  @staticmethod
  def generate_password_reset_token(email_address):
    user = User.query.filter_by(email_address=email_address).first()

    if user is None:
      return None

    # If the user has no token, or if the user has a token and it
    # has expired, generate a new token
    if (user.password_reset_token == "" or 
      (user.password_reset_token != "" and user.password_reset_token_expire < datetime.now())):
      token = uuid.uuid4().hex
      user.password_reset_token = token
      user.password_reset_token_expire = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() + timedelta(hours=24))
      db.session.add(user)
      db.session.commit()
    return user.password_reset_token


  # Save password by email address static function
  @staticmethod
  def save_password_by_email_address(email_address, password):
    user = User.query.filter_by(email_address=email_address).first()
    return True
        

  # Clear password reset token by email address static function
  @staticmethod
  def clear_password_token_by_email_address(email_address):
    user = User.query.filter_by(email_address=email_address).first()
    user.clear_password_token()
    return user


  # Clear user password reset static function
  @staticmethod
  def get_user_by_reset_token(reset_token):
    user = User.query.filter_by(password_reset_token=reset_token).first()
    return user


def authenticate(email_address, password):

  # Find the user by email address
  user = User.get_user_by_email_address(email_address)

  # If user is None then raise an Exception
  if user is None:
    raise UserUnknownException
