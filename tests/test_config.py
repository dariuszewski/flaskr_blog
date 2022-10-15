import os


def test_base_config(app):
    app.config.from_object('flaskr.config.Config')
    assert not app.config['TESTING']
    assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']


def test_development_config(app):
    app.config.from_object('flaskr.config.DevelopmentConfig')
    assert not app.config['TESTING']
    assert app.config['SECRET_KEY'] == 'dev'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///flaskr.sqlite'


# def test_production_config(app):
#     app.config.from_object('flaskr.config.ProductionConfig')
#     assert 1 == 1