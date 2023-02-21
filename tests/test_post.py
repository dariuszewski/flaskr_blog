# test_blog.py


import io

import pytest

from flaskr.models.post import Post
from flaskr.models.comment import Comment

from flaskr.blueprints.blog.comment import get_comment


# Given:
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path): 
    # Tests if not logged in user will be correctly redirected.
    # When:
    response = client.post(path)
    # Then
    assert response.headers["Location"] == "/auth/login"

    
def test_author_required(client, auth, database):
    # Tests if not logged in as author will be correctly redirected.
    # When: 'other' user with id=2 logged in.
    auth.login(username='other', password='test')
    # Then:
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # Then: Current user doesn't see edit link.
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path, database):
    # Test status code on paths to not existing post.
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, database):
    # Given: logged in user and working endpoint.
    auth.login()
    # Then: Can create a post.
    assert client.get('/create').status_code == 200
    # When: Posting data.
    client.post('/create', 
                data={'title': 'created', 'body': 'created', 'tags': 'created', 'photo': (io.BytesIO(b"abcdef"), '')},
                content_type='multipart/form-data')
    # Then: Title available in list of titles.
    assert 'created' in list(*zip(*database.session.execute(database.select(Post.title)).all()))


def test_update(client, auth, database):
    # When: 'test' user with id=1 logged in.
    auth.login()
    # Assert: User can upadate post with author_id=1.
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', 
                data={'title': 'updated', 'body': 'updated', 'tags': 'updated', 'photo': (io.BytesIO(b"abcdef"), '')},
                content_type='multipart/form-data')
    # Assert post with id=1 have title 'updated'.
    assert Post.get_post_by_id(1).title == 'updated'
    assert 'tag1' not in Post.get_post_by_id(1).tags


@pytest.mark.parametrize(
    ('path', 'title', 'body', 'tags', 'photo', 'message'), (
    ('/create','', '', '', '', 'Title is required.'),
    ('/create', 'Title', '', '', '', 'Body is required.'),
    ('/create', 'Title', 'Body', '', '', 'At least 1 tag is required.'),
    # ('/create', 'Title', 'Body', 'Tag', (io.BytesIO(b"abcdef"), 'test'*1000), 'Request Entity Too Large'),
    ('/1/update', '', '', '', '', 'Title is required.'),
    ('/1/update', 'Title', '', '','', 'Body is required.'),
    ('/1/update', 'Title', 'Body', '', '', 'At least 1 tag is required.'),
    # ('/1/update', 'Title', 'Body', 'Tag', (io.BytesIO(b"abcdef"), 'test'*1000), 'Request Entity Too Large'),
))
def test_create_update_validate(client, auth, database, path, title, body, tags, photo, message):
    # Test if validation of input works.
    auth.login()
    if not photo:
        photo = (io.BytesIO(b"abcdef"), '')
    response = client.post(path, data={'title': title, 'body': body, 'tags': tags, 'photo': photo},
                           content_type='multipart/form-data')
    assert bytes(message, encoding='utf-8') in response.data


def test_delete(client, auth, app, database):
    # The delete view should redirect to the index URL and the post should no longer exist in the database.
    # Given: user is logged in.
    auth.login()
    # When: Post is deleted.
    response = client.post('/1/delete')
    # Then: Redirected to index.
    assert response.headers["Location"] == "/"
    # Then: Post with id=1 doesn't exist in the database.
    assert Post.get_post_by_id(1) is None


def test_read(client, auth, database):
    # Given: user is not logged in.
    # When:
    response = client.get('/1/read')
    # Then: Anyone can read post.
    assert b'href="/1/update"' not in response.data
    assert b'Post #1' in response.data

    # Given: User is logged in and there is a post and predefined database.
    auth.login()
    # When:
    response = client.get('/1/read')
    # Then:
    assert b'href="/1/update"' in response.data


