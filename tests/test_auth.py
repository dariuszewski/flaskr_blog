import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    # Check if GET request returns correct status code.
    assert client.get('/auth/register').status_code == 200
    # Register a user 'a' with password 'a'
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    # Check if the user was redirected correctly.
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        # Check if user was created.
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


# Decorator tells Pytest to run the same test function with different arguments. (This acts as Given)
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    # Test if applications returns correct responses.
    # When
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    # Then
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        # Using client in a with block allows accessing context variables such as session after the response is returned. 
        # Normally, accessing session outside of a request would raise an error.
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    # Testing logout is the opposite of login. session should not contain user_id after logging out.
    auth.login() # Simulating user login with AuthActions.

    with client:
        auth.logout() # Simulating user logout with AuthActions.
        assert 'user_id' not in session