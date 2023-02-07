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


def test_tag(client, auth, database):
    auth.login()
    client.post('/create', data={'title': 'Post1', 'body': 'Body1', 'tags': 'tag1'})
    client.post('/create', data={'title': 'Post2', 'body': 'Body2', 'tags': 'tag2'})
    response = client.get('/index?tag=tag2')
    assert b'tag1' not in response.data
    assert b'tag2' in response.data


def test_successful_search(client, auth, database):
    auth.login()
    client.post('/create', data={'title': 'Post1', 'body': 'Body1', 'tags': 'tag1'})
    client.post('/create', data={'title': 'Post2', 'body': 'Body2', 'tags': 'tag2'})
    response = client.get('/index?keyword=Body1')
    assert b'Body2' not in response.data
    assert b'Body1' in response.data


def test_failed_search(client, auth, database):
    auth.login()
    client.post('/create', data={'title': 'Post1', 'body': 'Body1', 'tags': 'tag1'})
    client.post('/create', data={'title': 'Post2', 'body': 'Body2', 'tags': 'tag2'})
    response = client.get('/index?keyword=Body100')
    assert b"posts matching criterium: " in response.data
