import json
import unittest

from project.server.models import User
from flask_testing import TestCase
from project.server import create_app, db
from project.tests.base import BaseTestCase

app = create_app()

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

class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self, 'test@test.com', 'Test', 'Doe', 'password', 'teller')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Your account was registered successfully. You can now log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = User(
            email='test@test.com',
            password='password',
            first_name='Test',
            last_name='Doe',
            role='teller'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = register_user(self, 'test@test.com', 'Test', 'Doe', 'password', 'teller')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exist. Please try again')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)
    def test_registered_user_login(self):
        """ Test for login of registered-user login """
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
            data = json.loads(response.data.decode())
            self.assertTrue(data['role'])
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid credentials.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        """ Test for user status """
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
            ## Get Users
            response = self.client.get(
                '/api/auth/user',
                headers=dict(
                    Authorization='Bearer ' +login_data['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data is not None)
            self.assertTrue(data['id'] is not None)
            self.assertTrue(data['email'] == 'test@test.com')
            self.assertTrue(data['first_name'] == 'Test')
            self.assertTrue(data['last_name'] == 'Doe')
            self.assertTrue(data['role'] == 'teller')
            self.assertEqual(response.status_code, 200)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token"""
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
            response = self.client.get(
                '/api/auth/user',
                headers=dict(
                    Authorization='Bearer' + login_data['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['msg'] == "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'")
            self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()

