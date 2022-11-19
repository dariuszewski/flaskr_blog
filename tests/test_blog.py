# test_blog.py

import pytest

from flaskr.models.post import Post
from flaskr.models.comment import Comment

from flaskr.blog import get_comment

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
    assert b'href="/1/update"' in response.data


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
    client.post('/create', data={'title': 'created', 'body': ''})
    # Then: Title available in list of titles.
    assert 'created' in list(*zip(*database.session.execute(database.select(Post.title)).all()))


def test_update(client, auth, database):
    # When: 'test' user with id=1 logged in.
    auth.login()
    # Assert: User can upadate post with author_id=1.
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})
    # Assert post with id=1 have title 'updated'.
    assert Post.get_post_by_id(1).title == 'updated'


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path, database):
    # Test if validation of input works.
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


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


def test_like(client, auth, database):
    # Given: Not logged in user.
    # When: Likes post.
    response = client.post('/1/like')
    # Assert: Post #1 have only 1 like (which was preloaded).
    assert len(Post.get_post_by_id(1).likes) == 1 
    # Given: Logged in user which didn't like the post before.
    auth.login()
    # When: Likes post.
    response = client.post('/1/like')
    # Assert: New like was registered.
    assert len(Post.get_post_by_id(1).likes) == 2
    # When: Same user likes posts again.
    response = client.post('/1/like')
    # Assert: Post #1 have only 1 like - dislike was registered.
    assert len(Post.get_post_by_id(1).likes) == 1


def test_likers(client, auth, database):
    # Given: Logged in user which didn't like the post before.
    auth.login()
    # When: Checks who liked the post.
    response = client.get('/1/likers')
    # Assert: '1' is returned in json object.
    assert '1' in str(response.data)


def test_comment_not_logged_in(client, database):
    # Given: No user logged in.
    # When: Single post page.
    response = client.get('/1/read')
    # Assert: No comments added yet.
    assert b'No comments yet...' in response.data
    
    # When: Adding new comment at the root level.
    response = client.post('/1/read', 
        data={'body': 'test1', 'parent_id': -1})
    # Assert: Not logged in user can't add a comment.
    assert response.status_code == 403


def test_comment(client, auth, database):
    # Given: No user logged in.
    auth.login()    
    # When: Single post page.
    response = client.get('/1/read')
    # Assert: No comments added yet.
    assert b'No comments yet...' in response.data

    #When: Adding top-level comment with no body.
    response = client.post('/1/read', 
        data={'body': '', 'parent_id': -1})
    # Assert response.
    assert b'Body is required.' in response.data

    #When: Adding comment top-level with body.
    response = client.post('/1/read', 
        data={'body': 'Top level comment.', 'parent_id': -1, 'reply': 'Save'})
    # Assert response.
    assert b'Your comment has been added.' in response.data

    #When: Adding comment below top-level with body.
    response = client.post('/1/read', 
        data={'body': 'Top level comment.', 'parent_id': 1, 'reply': 'Save'})
    # Assert response.
    assert b'Your comment has been added.' in response.data

    #When: Adding comment below top-level with body.
    response = client.post('/1/read', 
        data={'body': 'Top level comment EDITED.', 'parent_id': 1, 'edit': 'Save'})
    # Assert response.
    assert b'Your comment has been edited.' in response.data



def test_comment_deletion(client, auth, database):
    # Given
    auth.login()
    client.post('/1/read', 
        data={'body': 'top level', 'parent_id': -1, 'reply': 'Save'})
    client.post('/1/read', 
        data={'body': '2nd level', 'parent_id': 1, 'reply': 'Save'})
    client.post('/1/read', 
        data={'body': '3rd level', 'parent_id': 2, 'reply': 'Save'})

    auth.logout()
    auth.login(username='other', password='test')

    # When: Not owner of comment tries to delete.
    response = client.get('/1/delete_comment?post_id=1')
    # Then
    assert response.status_code == 403

    # When owner tries to delete comment.
    auth.logout()
    auth.login()
    client.get('/1/delete_comment?post_id=1')
    response = client.get('/1/read')

    # Assert
    assert b'No comments yet...' in response.data

    # Assert when trying to delete non existing comment
    assert client.get('/1/delete_comment?post_id=1').status_code == 404 
    

def test_recursive_delete(client, auth, database):
        # Given
    auth.login()
    client.post('/1/read', 
        data={'body': 'top level', 'parent_id': -1, 'reply': 'Save'})
    client.post('/1/read', 
        data={'body': '2nd level', 'parent_id': 1, 'reply': 'Save'})
    client.post('/1/read', 
        data={'body': '3rd level', 'parent_id': 2, 'reply': 'Save'})

    # When
    comment = Comment.get_comment_by_id(1)
    Comment.recursive_delete(comment)
    response = client.get('/1/read')
    # Assert
    assert b'No comments yet...' in response.data

