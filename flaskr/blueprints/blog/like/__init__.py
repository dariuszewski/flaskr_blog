from flask import (
    Blueprint, g, jsonify
)
from werkzeug.exceptions import abort

from flaskr.blueprints.auth import login_required
from flaskr.blueprints.blog.post import get_post
from flaskr.models.like import Like
from flaskr.extensions import db


bp = Blueprint('like', __name__)


@bp.route('/<int:post_id>/like', methods=('POST',))
@login_required
def like_action(post_id):
    # Check if post exists.
    post = get_post(post_id, check_author=False)
    like = Like.get_like_by_post_and_author(post_id=post_id, author_id=g.user.id)
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(post_id=post_id, author_id=g.user.id)
        like.save()
    like = Like.get_like_by_post_and_author(post_id=post_id, author_id=g.user.id)

    return jsonify({
        "likes": len(post.likes),
        "liked": bool(like)
    })


@bp.route('/<int:post_id>/likers', methods=('GET',))
def likers_action(post_id):
    
    # Check if post exists.
    post = get_post(post_id, check_author=False)
    likers = [like.user.username for like in post.likes]

    # Return amount of likes.
    return jsonify({
        "likers_count": len(post.likes),
        "likers": likers
    })
