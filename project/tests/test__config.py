import unittest

from flask import current_app
from flask_testing import TestCase
from project.server import create_app
from project.tests.base import BaseTestCase

app = create_app()

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config.get('SECRET_KEY') == 'secret key')
        self.assertTrue(app.config['DEBUG'] == True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///database.sqlite'
        )

class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.ProductionConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'] == False)

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config.get('SECRET_KEY') == 'secret key')
        self.assertTrue(app.config['DEBUG'] == True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
        )


if __name__ == '__main__':
    unittest.main()

