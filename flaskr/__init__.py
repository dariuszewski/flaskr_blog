import os

from flask import Flask
from flask_uploads import configure_uploads

# Application Factory Pattern. This can be called with 
#       dev: flask --app flaskr --debug run
#       prod: waitress-serve --host 127.0.0.1 --call 'flaskr:create_app'
#       docker: docker build --tag flaskr_blog .  +  docker run -p 8000:8080 -d flaskr_blog
# App will expect to have $env:APP_SETTINGS variable which contains Config Object (ex. flaskr.config.DevelopmentConfig). 
def create_app(test_config=None):
    # Create and configure the app. Run with flask --app flaskr --debug run
    app = Flask(__name__, instance_relative_config=True)
    # The instance folder is designed to not be under version control and be deployment specific. 
    # It’s the perfect place to drop things that either change at runtime or configuration files.

    # Override app.config.from_mapping()
    if test_config is None:
        # load the instance config if not testing
        app_settings = os.getenv('APP_SETTINGS') or 'flaskr.config.DevelopmentConfig'
        app.config.from_object(app_settings)
        app.config['UPLOADED_PHOTOS_DEST']  = app.root_path + "/static/img"
    else:
        # Special configuration for testing purposes. 
        app.config.from_mapping(test_config) 
        
    # Ensure the instance folder exists, this is only for sqlite.
    os.makedirs(app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # register extensions
    # Using this design pattern, no application-specific state is stored on the extension object,
    # so one extension object can be used for multiple apps.
    from flaskr.extensions import db, photos, ckeditor
    db.init_app(app)
    ckeditor.init_app(app)
    configure_uploads(app, photos)
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