from datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User, Parcel
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    decode_token
)
from flask_cors import cross_origin

from project.server.parcels.routes import parcels_schema

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    def post(self):
        try:
            post_data = request.get_json()
            email = post_data.get('email')
            first_name = post_data.get('first_name')
            last_name = post_data.get('last_name')
            password = post_data.get('password')
            role = post_data.get('role')

            user = User.query.filter_by(email=email).first()

            if user is None:
                user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    role=role
                )

                db.session.add(user)
                db.session.commit()

                reponseObject = {
                    'status': 'success',
                    'message': 'Your account was registered successfully. You can now log in.'
                }
                return make_response(jsonify(reponseObject)), 201
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User already exist. Please try again'
                }
                return make_response(jsonify(responseObject)), 202

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 400

class LogInAPI(MethodView):
    @cross_origin()
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        try:
            user = User.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(
                user.password, password
            ):
                auth_token = create_access_token(user.id)
                responseObject = {
                    'role': user.role,
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Invalid credentials.'
                }
                return make_response(jsonify(responseObject)), 401
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Could not login. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401

class UserAPI(MethodView):
    decorators = [jwt_required()]
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                  'status': 'fail',
                  'message': 'Bearer token malformed'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token= ''

        if auth_token:
            resp = decode_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp['sub']).first()
                responseObject = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role
                }
                return make_response(jsonify(responseObject))
            else:
                responseObject= {
                  'status': 'fail',
                  'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
          responseObject= {
            'status': 'fail',
            'message': 'Provide a valid auth token'
          }
          return make_response(jsonify(responseObject)), 401


auth_register_view = RegisterAPI.as_view('auth_register_api')
auth_login_view = LogInAPI.as_view('auth_login_api')
auth_user_view = UserAPI.as_view('auth_user_api')

auth_blueprint.add_url_rule(
    '/api/auth/register',
    view_func=auth_register_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/api/auth/login',
    view_func=auth_login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/api/auth/user',
    view_func=auth_user_view,
    methods=['GET']
)