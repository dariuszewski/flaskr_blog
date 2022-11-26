# test_blog.py

import pytest

from flaskr.models.post import Post
from flaskr.models.comment import Comment


def test_like(client, auth, database):
    # Given: Not logged in user.
    # When: Likes post.
    client.post('/1/like')
    # Assert: Post #1 have only 1 like (which was preloaded).
    assert len(Post.get_post_by_id(1).likes) == 1 
    # Given: Logged in user which didn't like the post before.
    auth.login()
    # When: Likes post.
    client.post('/1/like')
    # Assert: New like was registered.
    assert len(Post.get_post_by_id(1).likes) == 2
    # When: Same user likes posts again.
    client.post('/1/like')
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

