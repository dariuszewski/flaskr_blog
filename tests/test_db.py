# test_db.py


import pytest

from flaskr.extensions import db



def test_database_uri(app):
    # DATABASE URI for tests should be a temporary  (in-memory database).
    # Assert 
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
        

def test_query(app):
    assert db.session.execute(db.select(1)).scalar() == 1
        