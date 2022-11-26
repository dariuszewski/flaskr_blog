from flask import (
    Blueprint, g, redirect, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.blueprints.auth import login_required
from flaskr.models.comment import Comment


bp = Blueprint('comment', __name__)


@bp.route('/<int:id>/delete_comment', methods=('GET',))
@login_required
def delete_comment(id):
    # This will delete a comment with all it's subcomments!

    post_id = request.args.get('post_id')

    comment = get_comment(id)
    Comment.recursive_delete(comment)

    return redirect(url_for('post.read', id=post_id))


def get_comment(id, check_author=True):
    # get_comment is used by update and delete routes.
    comment = Comment.get_comment_by_id(id)

    if comment is None:
        abort(404, f"Comment id {id} doesn't exist.")

    if check_author and comment.author_id != g.user.id:
        abort(403)

    return comment  


def create_comment(body, author_id, post_id, parent):
    comment = Comment(body=body, author_id=author_id, post_id=post_id, parent=parent)
    comment.save()

def update_comment(comment, body):
    comment = get_comment(comment.id) # Check author.
    comment.body = body
    comment.save()