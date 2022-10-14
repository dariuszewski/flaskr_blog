# test_auth.py

import pytest
from flask import g, session

from flaskr.models import User

# Passing database to test allows usage even if its not used within a function/
def test_register(client):
    # Assert: GET request returns correct status code.
    assert client.get('/auth/register').status_code == 200
    # When: Register a user 'a' with password 'a'.
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    # Assert: application redirected correctly.
    assert response.headers["Location"] == "/auth/login"

    # Assert: Username 'a' in the database.
    assert User.get_user_by_username('a') is not None


# Decorator tells Pytest to run the same test function with different arguments. (This acts as Given)
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered')
))
def test_register_validate_input(database, client, username, password, message):
    # Test if application returns correct responses on registration.
    # User 'test' is loaded in the fixture.
    # When 
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    # Then
    assert message in response.data


def test_login(client, auth, database):
    assert client.get('/auth/login').status_code == 200
    response = client.post(
        '/auth/login',
        data = {'username': 'test', 'password': 'test'}
    )
    # Assert: redirection to index after login.
    assert response.headers["Location"] == "/"

    with client:
        # Using client in a with block allows accessing context variables such as session after the response is returned. 
        # Normally, accessing session outside of a request would raise an error.
        client.get('/')
        assert session['user_id'] == 1
        assert g.user.username == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, database, username, password, message):
    # Test if application returns correct responses on login.
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth, database):
    # Testing logout is the opposite of login. session should not contain user_id after logging out.
    auth.login() # Simulating user login with AuthActions.

    with client:
        auth.logout() # Simulating user logout with AuthActions.
        assert 'user_id' not in session