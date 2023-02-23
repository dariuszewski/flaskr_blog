import pytest
import io

from flaskr.models.post import Post
from flaskr.models.tag import Tag
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
    client.post('/create', data={'title': 'Post1', 'body': 'Body1', 'tags': 'tag1', 'photo': (io.BytesIO(b"abcdef"), '')}, content_type='multipart/form-data')
    client.post('/create', data={'title': 'Post2', 'body': 'Body2', 'tags': 'tag2', 'photo': (io.BytesIO(b"abcdef"), '')}, content_type='multipart/form-data')
    response = client.get('/?' + path)
    assert bytes(data_in, encoding='utf-8') in response.data
    assert bytes(data_not_in, encoding='utf-8') not in response.data


def test_pagination(client, auth, database):
    # Given: At least 6 posts
    for i in range(6):
        post = Post(title=f"Post{i}", body=f'Body{i}', image=None)
        post.tags = [Tag(body=f'test{i}')]
        post.save()
    # When:
    response = client.get('/')
    # Then:
    assert b'Post1' in response.data
    assert b'Post5' not in response.data
    # When:
    page_2 = client.get('/?page=2')
    # Then:
    page_2.status_code == 200
    assert b'Post5' in page_2.data
    assert b'Post1' not in page_2.data
