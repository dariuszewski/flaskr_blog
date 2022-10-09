import pytest
from flaskr.db import get_db


def test_index(client, auth):
    # Given: user is not logged in.
    # When:
    response = client.get('/')
    # Then:
    assert b"Log In" in response.data # If user is not logged in, he have "Log In" available in the response.
    assert b"Register" in response.data # If user is not logged in, he have "Register" available in the response.

    # Given:
    auth.login()
    # When:
    response = client.get('/')
    # Then:
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data # Post update is available in response (due to data inserted in setup).


# Given:
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path): # Tests if not logged in user will be correctly redirected.
    # When:
    response = client.post(path)
    # Then
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    # Given: logged in user and working endpoint.
    auth.login()
    assert client.get('/create').status_code == 200
    # When: posting data.
    client.post('/create', data={'title': 'created', 'body': ''})

    # Then: post exists in database.
    with app.app_context():
        db = get_db() # testing database
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    # The delete view should redirect to the index URL and the post should no longer exist in the database.
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None