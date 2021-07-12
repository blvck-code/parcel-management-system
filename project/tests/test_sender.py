import json
import unittest

from project.tests.base import BaseTestCase

customer_data = {
    'full_name': 'Mary Doe',
    'email': 'marydoe@gmail.com',
    'phone': '25470000000',
    'center': 'Siaya'
}


def register_user(self, email, first_name, last_name, password, role):
    return self.client.post(
        '/api/auth/register',
        data=json.dumps(dict(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role
        )),
        content_type='application/json',
    )


def login_user(self, email, password):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


def create_user(self, data, token):
    return self.client.post(
        '/api/customer/create',
        data=json.dumps(dict(
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            center=data.get('center')
        )),
        headers=dict(
            content_type='application/json',
            Authorization='Bearer ' + token
        ),

    )


class TestCustomerBlueprint(BaseTestCase):
    def test_create_user(self):
        """ Test Admin Can Create Customer """
        with self.client:
            # user registration
            response = register_user(self, 'test@test.com', 'Test', 'Doe', 'password', 'teller')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Your account was registered successfully. You can now log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            # registered user login
            response = login_user(self, 'test@test.com', 'password')
            login_data = json.loads(response.data.decode())
            self.assertTrue(login_data['role'])
            self.assertTrue(login_data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            # create customer
            response = create_user(self, customer_data, login_data['auth_token'])
            data = json.loads(response.data.decode())


if __name__ == '__main__':
    unittest.main()
