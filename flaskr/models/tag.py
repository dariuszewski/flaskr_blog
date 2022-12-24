from flaskr.extensions import db
from flaskr.models.post_tag import post_tag

# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(20), nullable=False)

    @staticmethod
    def get_all_tags():
        return db.session.execute(db.select(Tag)).scalars()

    @staticmethod
    def get_tags_by_bodies(params):
        return db.session.execute(db.select(Tag).where(Tag.body.in_(params))).scalars()

    def save(self):
        db.session.add(self)
        db.session.commit()