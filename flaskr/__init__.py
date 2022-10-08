import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # The instance folder is designed to not be under version control and be deployment specific. 
    # It’s the perfect place to drop things that either change at runtime or configuration files.
    # TODO: 'try to parametrize instance_relative_config variable to create staging and production environments'
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') # this is only if used sqlite
    )

    if test_config is None:  # this will override app.config.from_mapping()
        # load the instance config if not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load testing config when passed in
        app.config.from_mapping(test_config) # special configuration for testing purposes

    # ensure the instance folder exists
    # this is only for sqlite
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # create the database and initialize connection
    from . import db
    db.init_app(app)

    # register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app