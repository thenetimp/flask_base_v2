from flask_api import FlaskAPI
from flask import request, session, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Define objects.
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
# login_manager = LoginManager()


# Create the flash app
def create_app(enviroment="dev"):

  # Import the models so the database can be created
  # I am not crazy about this being here.  Hoping to
  # find a way to import all of them in one go within
  # the function.
  # from app.models import User
  import app.models

  # Create the flask api application
  app = FlaskAPI(__name__)

  # Configuration Information should move to file.
  if enviroment == "test":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test_database.db'
  else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/dev_database.db'

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = 'super-secret'

  # Instanciate the JWTManager
  JWTManager(app)

  # Make sure the database initializes the app
  db.app = app
  db.init_app(app)
  migrate.init_app(app, db)

  # Return the application
  return app


  @app.errorhandler(500)
  def internal_error(error):
    return { 'status': 'error', 'code': 'error_fatal_error', 'message': 'A fatal error has occured please check the logs for more information' }
    # db.session.rollback()
    # return render_template('500.html'), 500


  @app.route('/')
  def main():
    return { 'status': 'error', 'code': 'error_invalid_endpoint', 'message': 'This is an invalid endpoint' }


  # Load the blueprints
  load_blueprints(app)
  return app


# Manage blueprint loading
def load_blueprints(app):
  from app.blueprints.user_endpoint import user_endpoint
  app.register_blueprint(user_endpoint)
  return True