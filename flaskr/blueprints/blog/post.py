from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.blueprints.auth import login_required
from flaskr.blueprints.blog.comment import create_comment, update_comment
from flaskr.models.post import Post
from flaskr.models.comment import Comment
from flaskr.models.tag import Tag
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
    all_tags = Tag.get_all_tags()
    if request.method == 'POST':
        print('I got a post request')
        title = request.form['title']
        body = request.form['body']
        tags = validate_tags(request.form['tags'])
        error = None

        if not title:
            error = 'Title is required.'
        if not body:
            error = 'Body is required.'
        if not tags:
            error = 'At least 1 tag is required.'

        if error is not None:
            flash(error)
        else:
            print('I have no errors')
            post = Post(title=title, body=body, author_id=g.user.id)
            create_missing_tags(tags, all_tags)
            print("Missing tags created successfully!")
            current_post_tags = Tag.get_tags_by_bodies(tags)
            for tag in current_post_tags:
                print(tag.body)
                post.tags.append(tag)
            print('Tags associated with post!')
            post.save()
            print(post.tags)
            return redirect(url_for('index'))

    return render_template('blog/create.html', tags=all_tags)


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


def validate_tags(tagstream):
    tags = tagstream.split(',')
    if all(tags):
        tags = [tag.strip().lower() for tag in tags]
        tags = list(set(tags))
        print('Validated Tags: ' + str(tags))
        return tags 
    else:
        print('Validation failed')
        return False

def create_missing_tags(tags, all_tags):
    all_tags_contents = [tag.body for tag in all_tags]
    print(all_tags_contents)
    missing_tags = [tag for tag in tags if tag not in all_tags_contents]
    print(missing_tags)
    for tag_body in missing_tags:
        tag = Tag(body=tag_body)
        tag.save()