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
    ('tag=tag1', 'tag1', 'find posts matching criterium:'),
    ('tag=tag1000', 'find posts matching criterium:', 'dummy'),
    ('keyword=Body1', 'Body1', 'Body2'),
    ('keyword=Body1000', 'find posts matching criterium:', 'dummy'),
    ('tag=tag1&keyword=Body1', 'tag1', 'body2'),
    ('tag=tag1&keyword=Body100', 'and containing', 'criterium'),
))
def test_filters(client, auth, database, path, data_in, data_not_in):
    auth.login()
    client.post('/create', data={'title': 'Post1', 'body': 'Body1', 'tags': 'tag1'})
    client.post('/create', data={'title': 'Post2', 'body': 'Body2', 'tags': 'tag2'})
    response = client.get('/index?' + path)
    assert data_in in response.text
    assert data_not_in not in response.text
