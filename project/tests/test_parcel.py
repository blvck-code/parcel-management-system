import json
import unittest

from project.tests.base import BaseTestCase

parcel_data = {
    'customer_id': '2',
    'receiver_id': '3',
    'parcel': {
        'item': 'Laptop',
        'dispatch_date': '2020-10-25',
        'arrival_date': '2020-10-28',
        'cost': '400',
        'quantity': '4',
    }
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

def dispatch_parcel(self, data, token):
    return self.client.post(
        '/api/parcels/create',
        data=json.dumps(dict(
            post_data=data
        )),
        headers=dict(
            content_type='application/json',
            Authorization='Bearer ' + token
        )
    )

class TestParcelBlueprint(BaseTestCase):
    def test_user_can_dispatch_parcel(self):
        """ Test User Can Dispatch Parcel """
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
            # dispatch parcel
            response = dispatch_parcel(self, parcel_data, login_data['auth_token'])
            data = json.loads(response.data.decode())
            print(data)

    def test_admin_can_fetch_parcels(self):
        """ Test Admin Can Fetch Parcels API"""
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
            # fetch data
            response = self.client.get(
                '/api/parcels/list',
                headers=dict(
                    Authorization='Bearer' + login_data['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(response.status_code == 200)

    def test_fetch_parcels(self):
        """ Test Teller Can Fetch Parcels API"""
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
            # fetch data
            response = self.client.get(
                '/api/parcels/list',
                headers=dict(
                    Authorization='Bearer' + login_data['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(response.status_code == 200)

if __name__ == '__main__':
    unittest.main()


