from flaskr.extensions import db


post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey("post.id")),
    db.Column('tag_id', db.Integer, db.ForeignKey("tag.id"))
)