from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.models.post import Post
from flaskr.models.like import Like
from flaskr.models.comment import Comment
from flaskr.extensions import db


bp = Blueprint('blog', __name__)


@bp.route('/', methods=('GET',))
def index():
    posts = Post.get_all()
    return render_template('blog/index.html', posts=posts)



@bp.route('/<int:id>/read', methods=('GET', 'POST', 'DELETE'))
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

        else:
            comment = Comment(body=body, author_id=g.user.id, post_id=post.id, parent=parent)
            comment.save()
            flash('Your comment has been added.')

    return render_template('blog/read.html', post=post)


@bp.route('/<int:id>/delete_comment', methods=('GET',))
@login_required
def delete_comment(id):
    # This will delete a comment with all it's subcomments!

    post_id = request.args.get('post_id')

    comment = get_comment(id)
    Comment.recursive_delete(comment)

    return redirect(url_for('blog.read', id=post_id))

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
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    # get_post is used by update and delete routes.

    post = Post.get_post_by_id(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

def get_comment(id, check_author=True):
    # get_comment is used by update and delete routes.
    comment = Comment.get_comment_by_id(id)

    if comment is None:
        abort(404, f"Comment id {id} doesn't exist.")

    if check_author and comment.author_id != g.user.id:
        abort(403)

    return comment  


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
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))


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
