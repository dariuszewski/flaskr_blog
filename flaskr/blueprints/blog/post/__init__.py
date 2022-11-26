from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.blueprints.auth import login_required
from flaskr.blueprints.blog.comment import create_comment, update_comment
from flaskr.models.post import Post
from flaskr.models.comment import Comment
from flaskr.extensions import db


bp = Blueprint('post', __name__)


@bp.route('/<int:id>/read', methods=('GET', 'POST'))
def read(id, comment_id=None):

    # Checks if post exists.
    post = get_post(id, check_author=False)

    if request.method == 'POST':
        # Create comment.

        body = request.form['body']
        parent = Comment.get_comment_by_id(id=request.form['parent_id'])

        error = None

        if not g.user:
            abort(403)
            
        if not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)

        else: # can i update any post even if im not author?s
            if 'reply' in request.form:
                create_comment(body=body, author_id=g.user.id, post_id=post.id, parent=parent)
                flash('Your comment has been added.')
            if 'edit' in request.form:
                update_comment(comment=parent, body=body)
                flash('Your comment has been edited.')

    return render_template('blog/read.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=g.user.id)
            post.save()
            return redirect(url_for('index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


def get_post(id, check_author=True):
    # get_post is used by update and delete routes.

    post = Post.get_post_by_id(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post