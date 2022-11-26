# conftest.py
# Pytest uses fixtures by matching their function names with the names of arguments in the test functions.
# They are usually residing in conftest.py file.
# They don't have to be explicitly used in the testing function, it is enought to pass them as parameters.
# run oprions:
## coverage run -m pytest
## coverage html
## pytest tests/

import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.extensions import db
from flaskr.models.user import User
from flaskr.models.post import Post
from flaskr.models.like import Like


@pytest.fixture(scope="module") # This fixture is destroyed during teardown of the last test in the "module".
def app():
    # The app fixture will call the factory and pass test_config to configure the application and database for testing
    app = create_app({
        'TESTING': True, # Tells Flask that the app is in test mode to change some internal behavior. Other extensions can also use the flag.
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test'
    })

    with app.app_context():
        # Pass application context in case there is no request.
        yield app


@pytest.fixture
def database():
    # The database fixture will create all tables in testing app's db and insert testing data.
    # This is also test for werkzeug.security.
    db.create_all()
    ########################## TESTING DATA ##########################
    user = User(username='test', 
    password='pbkdf2:sha256:260000$5nA3Qw0INBKctANp$d02abb7c77f46bf38708c97a0fb8b3067c5944e85f04fb2b8e31164cf9562d62')
    user.save()
    user = User(username='other', 
    password='pbkdf2:sha256:260000$5nA3Qw0INBKctANp$d02abb7c77f46bf38708c97a0fb8b3067c5944e85f04fb2b8e31164cf9562d62')
    user.save()
    post = Post(title='test title', body='test\nbody', author_id=1)
    post.save()
    like = Like(post_id=1, author_id=2)
    like.save()
    ##################################################################
    yield db
    # Drop on teardown.
    db.session.remove()
    db.drop_all()

@pytest.fixture
def client(app):
    # Tests will use the client to make requests to the application without running the server.
    return app.test_client()


@pytest.fixture
def runner(app):
    # Creates a runner that can call the Click commands registered with the application.
    # It is currently not used but kept for future reference.
    return app.test_cli_runner()


class AuthActions(object):
    # For most of the views, a user needs to be logged in. 
    # The easiest way to do this in tests is to make a POST request to the login view with the client. 
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        # Login test client.
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        # Test logout.
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    # Allows to call auth.login() etc. in a test to log in as the test user.
    return AuthActions(client)
