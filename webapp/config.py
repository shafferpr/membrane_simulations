# defines the configuration class for the application, basically just
# initializes a few variables that the application uses, those variables
# can be access as application.config['x']

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'xYD/vlPB2E5eD54hyRe753+zqWuWKt27z3+VsE6j'
    CSRF_SESSION_KEY = 'qER/vlPA2E6eD54hyRl153+kqVxWKt27z9+VsE6j'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                          'app.db')
    # local database, if using this on a new machine,
    # you probably have to run flask db init before it's available

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
