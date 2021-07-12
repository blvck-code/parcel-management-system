import json
import unittest

from project.tests.base import BaseTestCase

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

def create_user(self, email, first_name, last_name, role, password, token):
    return self.client.post(
        '/api/users/create',
        data=json.dumps(dict(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            password=password
        )),
        headers=dict(
            content_type='application/json',
            Authorization='Bearer ' + token
        )
    )

class TestUserBlueprint(BaseTestCase):
    def test_get_users(self):
        """ Test Get Users with Admin """
        with self.client:
            # user registration
            response = register_user(self, 'test@test.com', 'Test', 'Doe', 'password', 'admin')
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
                '/api/users/list',
                headers=dict(
                    Authorization='Bearer ' + login_data['auth_token']
                )
            )
            self.assertTrue(response.status_code == 200)

    def test_get_users_with_unauthorised_user(self):
        """ Test Get Users with Not Admin """
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
                '/api/users/list',
                headers=dict(
                    Authorization='Bearer ' + login_data['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'You are not authorized to access this data.')
            self.assertTrue(response.status_code == 403)

    def test_create_user_by_admin(self):
        """ Test Admin Can Create User """
        with self.client:
            # user registration
            response = register_user(self, 'test2@test.com', 'Test', 'Doe', 'password', 'admin')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Your account was registered successfully. You can now log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            # registered user login
            response = login_user(self, 'test2@test.com', 'password')
            login_data = json.loads(response.data.decode())
            self.assertTrue(login_data['role'])
            self.assertTrue(login_data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            #create user
            response = self.client.post(
                        '/api/users/create',
                        data=json.dumps(dict(
                            email='jdoe3@gmail.com',
                            first_name='John',
                            last_name='Doe',
                            role='teller',
                            password='password'
                        )),
                        headers=dict(
                            content_type='application/json',
                            Authorization='Bearer ' + login_data['auth_token']
                        )
                    )
            data = json.loads(response.data.decode())
            # @todo ====> finish up on this test
            # self.assertTrue(data['email'] == 'mdoe@gmail.com')
            # self.assertTrue(data['message'] == 'You are not authorized to access this data.')
            # self.assertTrue(response.status_code == 200)

    def test_create_user_by_unauthorized_user(self):
        """ Test None Admin Cant Create User """
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
            #create user
            response = create_user(self, 'mdoe2@gmail.com', 'Mary', 'Doe', 'teller', 'password', login_data['auth_token'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'You are not authorized to access this data.')
            self.assertTrue(response.status_code == 403)

    def test_admin_can_fetch_users(self):
        """ Test Admin Can Fetch Users """
        with self.client:
            # user registration
            response = register_user(self, 'test@test.com', 'Test', 'Doe', 'password', 'admin')
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
            # get users
            response = self.client.get(
              '/api/users/list',
              headers=dict(
                content_type='application/json',
                Authorization='Bearer ' + login_data['auth_token']
              ))
            data = json.loads(response.data.decode())
            self.assertTrue(response.status_code == 200)

    def test_teller_cant_fetch_users(self):
        """ Test Teller Cant Fetch Users """
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
            # get users
            response = self.client.get(
              '/api/users/list',
              headers=dict(
                content_type='application/json',
                Authorization='Bearer ' + login_data['auth_token']
              ))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'You are not authorized to access this data.')
            self.assertTrue(response.status_code == 403)

    def test_unauthorised_cant_fetch_users(self):
        """ Test Unauthorised Cant Fetch Users """
        with self.client:
            # get users
            response = self.client.get(
              '/api/users/list',
              headers=dict(
                content_type='application/json',
              ))
            data = json.loads(response.data.decode())
            print(response.status_code)
            self.assertTrue(data['msg'] == 'Missing Authorization Header')
            self.assertTrue(response.status_code == 401)

if __name__ == '__main__':
    unittest.main()
