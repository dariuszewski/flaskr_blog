from os import stat
from sqlalchemy import desc

from flaskr.extensions import db


# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(120))

    posts = db.relationship("Post", back_populates='user')
    likes = db.relationship('Like', back_populates='user', passive_deletes=True)
    comments = db.relationship('Comment', back_populates='user', passive_deletes=True)


    @staticmethod
    def get_user_by_username(username):
        return db.session.execute(db.select(User).filter_by(username=username)).scalar()

    @staticmethod
    def get_user_by_id(id):
        return db.session.execute(db.select(User).filter_by(id=id)).scalar()

    def save(self):
        db.session.add(self)
        db.session.commit()
