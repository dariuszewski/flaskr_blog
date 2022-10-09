import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

# Pytest uses fixtures by matching their function names with the names of arguments in the test functions. 

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp() # Temporary file containing testing database instead of instance folder. Removed after testing.

    app = create_app({
        'TESTING': True, # Tells Flask that the app is in test mode to change some internal behavior. Other extensions can also use the flag.
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql) # Insert testing data to testing database.

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # Tests will use the client to make requests to the application without running the server.
    return app.test_client()


@pytest.fixture
def runner(app):
    # Creates a runner that can call the Click commands registered with the application.
    return app.test_cli_runner()


class AuthActions(object):
    # For most of the views, a user needs to be logged in. 
    # The easiest way to do this in tests is to make a POST request to the login view with the client. 
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        # Test client sends predefined test data to the endpoint.
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        # Test logout.
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    # Allows to call auth.login() in a test to log in as the test user.
    return AuthActions(client)