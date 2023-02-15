import pytest

from flaskr.models.post import Post
from flaskr.models.comment import Comment


def test_index(client, auth, database):
    # Given: user is not logged in.
    # When:
    response = client.get('/')
    # Then:
    assert b"Log In" in response.data # If user is not logged in, he have "Log In" available in the response.
    assert b"Register" in response.data # If user is not logged in, he have "Register" available in the response.

    # Given: User is logged in and there is a post and predefined database.
    auth.login()
    # When:
    response = client.get('/')
    # Then:
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on ' in response.data
    assert b'test\nbody' in response.data
    assert b'test1' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize(
    ('path', 'data_in', 'data_not_in'), (
    ('keyword=Body1', 'Body1', 'Body2'),
    ('keyword=Body1000', 'find posts matching criterium:', 'dummy'),
    ('tag=tag1', 'tag1', 'tag2'),
    ('tag=tag1000', 'find posts matching criterium:', 'dummy'),
))
def test_filters(client, auth, database, path, data_in, data_not_in):
    auth.login()
    client.post('/create', data={'title': 'Post1', 'body': 'Body1', 'tags': 'tag1'})
    client.post('/create', data={'title': 'Post2', 'body': 'Body2', 'tags': 'tag2'})
    response = client.get('/index?' + path)
    assert data_in in response.text
    assert data_not_in not in response.text


def test_pagination(client, auth, database):
    auth.login()
    client.post('/create', data={'title': 'Post1', 'body': 'Body1', 'tags': 'tag1'})
    client.post('/create', data={'title': 'Post2', 'body': 'Body2', 'tags': 'tag2'})
    client.post('/create', data={'title': 'Post3', 'body': 'Body3', 'tags': 'tag3'})
    client.post('/create', data={'title': 'Post4', 'body': 'Body4', 'tags': 'tag4'})
    client.post('/create', data={'title': 'Post5', 'body': 'Body5', 'tags': 'tag5'})
    client.post('/create', data={'title': 'Post6', 'body': 'Body6', 'tags': 'tag6'})
    response = client.get('/index')
    assert 'tag1' in response.text
    assert 'tag6' not in response.text
    response = client.get('/index?page=2')
    assert 'tag6' in response.text
    assert 'tag1' not in response.text

