from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app(
        {'TESTING': True, 
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'UPLOADED_PHOTOS_DEST': "/static/test/img"
        }).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'


def test_database_uri(app):
    # DATABASE URI for tests should be a temporary  (in-memory database).
    # Assert 
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'