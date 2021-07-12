from flask_testing import TestCase
from project.server import db, create_app
from project.server.config import TestingConfig

app = create_app()

class BaseTestCase(TestCase):
    """ Base Test """
    def create_app(self):
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()