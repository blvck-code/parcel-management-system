from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask import Blueprint, make_response, jsonify, request

from project.server import db
from project.server.models import Sender
from project.server.parcels.routes import get_customer_id

customer_blueprint = Blueprint('customer', __name__)

class CreateCustomerAPI(MethodView):
    decorator = [jwt_required(), cross_origin()]
    def post(self):
        try:
            post_data = request.get_json()

            full_name = post_data.get('full_name')
            email = post_data.get('email')
            phone = post_data.get('phone')
            center = post_data.get('center')

            customer = Sender(
                full_name=full_name,
                phone=phone,
                email=email,
                center=center
            )

            db.session.add(customer)
            db.session.commit()
            get_customer_id(customer)

            responseObject = {
                'status': 'success',
                'message': 'Customer created successfully',
                'customer_id': customer.id
            }

            return make_response(jsonify(responseObject)), 201

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Could not add customer. Please try again.'
            }
            return make_response(jsonify(responseObject)), 400



customer_create_view = CreateCustomerAPI.as_view('customer_create_api')

customer_blueprint.add_url_rule(
    '/api/customer/create',
    view_func=customer_create_view,
    methods=['POST']
)