import os

from flask import Flask


# Application Factory Pattern
# This can be called with a parameter such as flask run --app flaskr:create_app(test_config=True)
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # The instance folder is designed to not be under version control and be deployment specific. 
    # It’s the perfect place to drop things that either change at runtime or configuration files.
    # TODO: 'try to parametrize instance_relative_config variable to create staging and production environments'
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite') # this is only if used sqlite
    )
    print(app.config["SQLALCHEMY_DATABASE_URI"])
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

    # register extensions
    # Using this design pattern, no application-specific state is stored on the extension object,
    # so one extension object can be used for multiple apps.
    from flaskr.extensions import db
    db.init_app(app)
    # Create the database tables in the app context (since no request is available at this stage).
    # This doesn't update existing tables (use Alembic to do that).
    with app.app_context():
        db.create_all()

    # register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app