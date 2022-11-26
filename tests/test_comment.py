# test_blog.py

import pytest

from flaskr.models.comment import Comment


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

    # Given: User which is not an author of comment.
    auth.logout()
    auth.login('other', 'test')
    # When: Trying to update comment
    response = client.post('/1/read', 
        data={'body': 'Top level comment EDITED TWICE.', 'parent_id': 1, 'edit': 'Save'})
    # Then: Not allowed
    assert response.status_code == 403

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


