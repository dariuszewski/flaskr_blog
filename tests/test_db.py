import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    # Within an application context, get_db should return the same connection each time it’s called.
    # Given: app context.
    with app.app_context():
        # When: connection with db.
        db = get_db()
        # Then: connection is a same object everytime it's called.
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    # The init-db command should call the init_db function and output a message.
    class Recorder(object): 
        # Recorder object is used to record if init-db was executed.
        called = False

    def fake_init_db():
        # fake_init_db method is used to replace init-db in tests
        Recorder.called = True
    # Given
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db) # Replaces init_db with fake_init_db
    # When
    result = runner.invoke(args=['init-db']) # test runner executes command init-db (which executes init_db), which is replaced by fake_init_db
    assert 'Initialized' in result.output
    assert Recorder.called