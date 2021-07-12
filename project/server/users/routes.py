from datetime import datetime
from flask import Blueprint, make_response, jsonify, request
from flask.views import MethodView
from flask_marshmallow import Marshmallow

from project.server import ma, db
from project.server.models import User
from flask_cors import cross_origin
from flask_jwt_extended import get_jwt_identity, jwt_required

user_blueprint = Blueprint('users', __name__)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'registered_on', 'role')

users_schema = UserSchema(many=True)

class ListUserAPI(MethodView):
    decorators = [jwt_required(), cross_origin()]
    def get(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'admin':
            try:
                users = User.query.order_by(User.id.desc())
                print(users)
                result = users_schema.dump(users)
                return make_response(jsonify(result)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Could not get users. Please try again'
                }
                return make_response(jsonify(responseObject)), 400
        else:
            responseObject = {
                'status': 'fail',
                'message': 'You are not authorized to access this data.'
            }
            return make_response(jsonify(responseObject)), 403

class CreateUserAPI(MethodView):
    decorators = [jwt_required(), cross_origin()]
    def post(self):
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'admin':
            try:
                post_data = request.get_json()

                first_name = post_data.get('first_name')
                last_name = post_data.get('last_name')
                email = post_data.get('email')
                password = post_data.get('password')
                role = post_data.get('role')
                print(email)

                user = User.query.filter_by(email=email).first()
                print(user)
                if user:
                    responseObject = {
                        'status': 'fail',
                        'message': 'User with that email already exists. Please try again'
                    }
                    return make_response(jsonify(responseObject)), 400

                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    role=role
                )

                db.session.add(user)
                db.session.commit()

                responseObject = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role
                }

                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Could not add the user. Please try again'
                }
                return make_response(jsonify(responseObject)), 400
        else:
            responseObject = {
                'status': 'fail',
                'message': 'You are not authorized to access this data.'
            }
            return make_response(jsonify(responseObject)), 403

users_list_view = ListUserAPI.as_view('users_list_api')
users_create_view = CreateUserAPI.as_view('users_create_api')

user_blueprint.add_url_rule(
    '/api/users/list',
    view_func=users_list_view,
    methods=['GET']
)

user_blueprint.add_url_rule(
    '/api/users/create',
    view_func=users_create_view,
    methods=['POST']
)
