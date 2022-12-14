import os

from flask import Flask


# Application Factory Pattern. This can be called with flask --app flaskr --debug run
# App will expect to have $env:APP_SETTINGS variable which contains Config Object (ex. flaskr.config.DevelopmentConfig). 
def create_app(test_config=None):
    # Create and configure the app. Run with flask --app flaskr --debug run
    app = Flask(__name__, instance_relative_config=True)
    # The instance folder is designed to not be under version control and be deployment specific. 
    # It’s the perfect place to drop things that either change at runtime or configuration files.

    os.environ["APP_SETTINGS"] = 'flaskr.config.DevelopmentConfig' #
    # Override app.config.from_mapping()
    if test_config is None:
        # load the instance config if not testing
        app_settings = os.getenv('APP_SETTINGS') or 'flaskr.config.DevelopmentConfig'
        app.config.from_object(app_settings)
    else:
        # Load testing config when passed in. 
        app.config.from_mapping(test_config) # Special configuration for testing purposes.

    # Ensure the instance folder exists, this is only for sqlite.
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
        from flaskr.models.user import User
        from flaskr.models.post import Post
        from flaskr.models.like import Like
        from flaskr.models.comment import Comment
        from flaskr.models.tag import Tag 
        from flaskr.models.post_tag import post_tag
        db.create_all()

    # register blueprints
    from .blueprints import auth
    app.register_blueprint(auth.bp)

    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')

    from .blueprints.blog import index
    from .blueprints.blog import like
    from .blueprints.blog import post
    from .blueprints.blog import comment

    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(post.bp)
    app.register_blueprint(comment.bp)
    app.register_blueprint(like.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app