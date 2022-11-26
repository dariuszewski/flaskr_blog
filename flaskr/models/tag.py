from os import stat
from sqlalchemy import desc

from flaskr.extensions import db
from flaskr.models.post_tag import post_tag

# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(20), nullable=False)

    posts = db.relationship('Post', secondary=post_tag, backref='post')

    @staticmethod
    def get_all_tags():
        return db.session.execute(db.select(Tag)).scalars()

    def save(self):
        db.session.add(self)
        db.session.commit()