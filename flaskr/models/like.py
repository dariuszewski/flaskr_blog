from os import stat
from sqlalchemy import desc

from flaskr.extensions import db


# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship('User', back_populates="likes", passive_deletes=True)
    post = db.relationship('Post', back_populates="likes", passive_deletes=True)

    @staticmethod
    def get_like_by_post_and_author(post_id, author_id):
        return db.session.execute(db
            .select(Like)
            .filter_by(post_id=post_id, author_id=author_id)).scalar()

    def save(self):
        db.session.add(self)
        db.session.commit()