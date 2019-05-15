import json
from flask import Blueprint
from flask import request, session, redirect, url_for, jsonify
from app.models import User
from app.exceptions.user_exceptions import UserExistsException

# User Endpoint blueprint
user_endpoint = Blueprint('user', __name__)


##############################
# GET list of user object
##############################
@user_endpoint.route('/users', methods=['GET'])
def page_users_get():
    return {'users': 'get'}


##############################
# GET user object
##############################
@user_endpoint.route('/user', methods=['GET'])
def page_user_get():
    return {'user': 'get'}


##############################
# POST user object
##############################
@user_endpoint.route('/user', methods=['POST'])
def page_user_post():
  try:
    user = User.create_user(request.data['first_name'], request.data['last_name'], request.data['email_address'], request.data['password'])
    response =  {'first_name': user.first_name }
  except UserExistsException as exception:
    response =  exception.error
  return response


##############################
# PUT the user object
##############################
@user_endpoint.route('/user', methods=['PUT'])
def page_user_put():
    return {'user': 'put'}    


##############################
# DELETE the user object
##############################
@user_endpoint.route('/user', methods=['DELETE'])
def page_user_delete():
    return {'error': 'delete'}
