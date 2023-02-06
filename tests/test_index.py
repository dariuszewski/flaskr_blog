from flaskr.models.post import Post
from flaskr.models.comment import Comment


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
