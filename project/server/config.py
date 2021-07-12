
class BaseConfig(object):
    """ Base Configurations """
    DEBUG = False
    SECRET_KEY = 'RIDZDrp94DRPcyZGqjn0CTbFtZ6qFE2bpCTNmPYM'
    CORS_HEADERS = 'Content-Type'
    JWT_SECRET_KEY = "leDqP8cc8MNoqSXXmvfjWuau8OowRXavyw"
    BCRYPT_LOGS_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    PAGINATE_PAGINATION_OBJECT_KEY = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """ Development Configurations """
    DEBUG = True
    BCRYPT_LOGS_ROUNDS = 4

class TestingConfig(BaseConfig):
    """ Testing Configurations """
    DEBUG = True
    TESTING = True
    BCRYPT_LOGS_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    """ Production Configurations """
    DEBUG = False