from os import stat
from sqlalchemy import desc

from flaskr.extensions import db
from flaskr.models.post_tag import post_tag

# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship('User', back_populates="posts")
    likes = db.relationship('Like', back_populates="post", passive_deletes=True)
    comments = db.relationship('Comment', back_populates='post', passive_deletes=True)
    tags = db.relationship('Tag', secondary=post_tag)

    @staticmethod
    def get_all():
        return db.session.execute(db
            .select(Post)
            .order_by(desc(Post.created))).scalars()

    @staticmethod
    def get_post_by_id(id):
        return db.session.execute(db
            .select(Post)
            .filter_by(id=id)).scalar()

    def save(self):
        db.session.add(self)
        db.session.commit()


