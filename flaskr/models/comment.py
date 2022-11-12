from os import stat
from sqlalchemy import desc

from flaskr.extensions import db


# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class Comment(db.Model):
    __tablename__ = 'comment'
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now()) 

    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))
    user = db.relationship('User', back_populates="comments", passive_deletes=True)
    post = db.relationship('Post', back_populates="comments", passive_deletes=True)


    @staticmethod
    def get_comment_by_id(id):
        return db.session.execute(db
            .select(Comment)
            .filter_by(id=id)).scalar()
    
    @staticmethod
    def get_comments_by_parent_id(parent_id):
        return db.session.execute(db
            .select(Comment)
            .filter_by(parent_id=parent_id)).scalars()        

    @staticmethod
    def recursive_delete(parent):
        children = Comment.get_comments_by_parent_id(parent.id)
        children = [child for child in children]
        for child in children:
            Comment.recursive_delete(child)
            db.session.delete(child)
            db.session.commit()
        db.session.delete(parent)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()