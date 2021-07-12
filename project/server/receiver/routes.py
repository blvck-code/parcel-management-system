from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask import Blueprint, make_response, jsonify, request

from project.server import db
from project.server.models import Receiver
from project.server.utils import get_recipient_id

receiver_blueprint = Blueprint('receiver', __name__)

class CreateReceiverAPI(MethodView):
    decorator = [jwt_required(), cross_origin()]
    def post(self):
        try:
            post_data = request.get_json()

            full_name = post_data.get('full_name')
            email = post_data.get('email')
            phone = post_data.get('phone')
            center = post_data.get('center')

            receiver = Receiver(
                full_name=full_name,
                phone=phone,
                email=email,
                center=center
            )

            db.session.add(receiver)
            db.session.commit()
            get_recipient_id(receiver)

            responseObject = {
                'status': 'success',
                'message': 'Receiver created successfully',
                'receiver_id': receiver.id
            }

            return make_response(jsonify(responseObject)), 201

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Could not add customer. Please try again.'
            }
            return make_response(jsonify(responseObject)), 400



receiver_create_view = CreateReceiverAPI.as_view('receiver_create_api')

receiver_blueprint.add_url_rule(
    '/api/receiver/create',
    view_func=receiver_create_view,
    methods=['POST']
)