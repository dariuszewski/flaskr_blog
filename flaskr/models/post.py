from os import stat
from sqlalchemy import desc, or_

from flaskr.extensions import db
from flaskr.models.post_tag import post_tag
from flaskr.models.tag import Tag
from flaskr.models.user import User

# SQLAlchemy automatically defines an __init__ method for each model that assigns 
# any keyword arguments to corresponding database columns and other attributes.


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    image = db.Column(db.String(120), nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship('User', back_populates="posts")
    likes = db.relationship('Like', back_populates="post", passive_deletes=True)
    comments = db.relationship('Comment', back_populates='post', passive_deletes=True)
    tags = db.relationship('Tag', secondary=post_tag)

    @staticmethod
    def get_all(page=1, per_page=5):
        return db.paginate(db
            .select(Post)
            .order_by(desc(Post.created)),
            page=page, per_page=per_page)


    @staticmethod
    def get_post_by_id(id):
        return db.session.execute(db
            .select(Post)
            .filter_by(id=id)).scalar()

    @staticmethod
    def get_posts_by_phrase(keyword, page=1, per_page=5):
        keyword = f'%{keyword}%'
        return db.paginate(db
            .select(Post)
            .join(User)
            .join(post_tag).join(Tag)
            .distinct()
            .order_by(desc(Post.created))
            .filter(or_(
                Post.title.ilike(keyword), 
                Post.body.ilike(keyword),
                User.username.ilike(keyword),
                Tag.body.ilike(keyword)
                )),
            page=page, per_page=per_page)

    @staticmethod
    def get_posts_by_tag(tag, page=1, per_page=5):
        return db.paginate(db
            .select(Post)
            .join(post_tag).join(Tag)
            .distinct()
            .filter(Tag.body == tag),
            page=page, per_page=per_page)

    def save(self):
        db.session.add(self)
        db.session.commit()


