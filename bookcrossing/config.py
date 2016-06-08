import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
	SECRET_KEY = 'my_secret_key_here'
	DEBUG = False
	BCRYPT_LOG_ROUNDS = 13
	WTF_CSRF_ENABLED = True
	DEBUG_TB_ENABLED = False
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	STATIC_FOLDER = os.path.join(BASE_DIR, 'static')


class DevelopmentConfig(BaseConfig):
	DEBUG = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.sqlite')
	DEBUG_TB_ENABLED = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
	TESTING = True
	DEBUG = True
	BCRYPT_LOG_ROUNDS = 1
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
	SECRET_KEY = 'my_super_secret_key_here'
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
	DEBUG_TB_ENABLED = False
	STRIPE_SECRET_KEY = 'foo'
	STRIPE_PUBLISHABLE_KEY = 'bar'


def runtime_config(status):
	if status == 'dev':
		return DevelopmentConfig

	if status == 'prod':
		return ProductionConfig

	if status == 'test':
		return TestingConfig

	return BaseConfig