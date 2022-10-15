from sqlalchemy import desc

from flaskr.extensions import db


# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))

    posts = db.relationship("Post")


    @staticmethod
    def get_user_by_username(username):
        return db.session.execute(db.select(User).filter_by(username=username)).scalar()

    @staticmethod
    def get_user_by_id(id):
        return db.session.execute(db.select(User).filter_by(id=id)).scalar()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    @staticmethod
    def get_posts_and_usernames():
        return db.session.execute(db
            .select(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username)
            .join(Post, User.posts)
            .order_by(desc(Post.created))).all()
    
    @staticmethod
    def get_post_by_id(id):
        return db.session.execute(db.select(Post).filter_by(id=id)).scalar()

    def save(self):
        db.session.add(self)
        db.session.commit()

