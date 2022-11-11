from os import stat
from sqlalchemy import desc

from flaskr.extensions import db


# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now()) 

    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    parent = db.relationship('Comment', remote_side=[id])
    user = db.relationship('User', back_populates="comments", passive_deletes=True)
    post = db.relationship('Post', back_populates="comments", passive_deletes=True)

    @staticmethod
    def get_comments_by_post(post_id):
        return db.session.execute(db
            .select(Comment)
            .filter_by(post_id=post_id)).all()
    
    @staticmethod
    def get_child_comments(post_id):
        return db.session.execute(db
            .select(Comment)
            .filter_by(parent_id=post_id)
            .order_by(Comment.created)).scalars()

    def save(self):
        db.session.add(self)
        db.session.commit()