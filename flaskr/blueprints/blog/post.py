import uuid
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from flask_uploads import extension
from werkzeug.exceptions import abort
from PIL import Image

from flaskr.blueprints.auth import login_required
from flaskr.blueprints.blog.comment import create_comment, update_comment
from flaskr.models.post import Post
from flaskr.models.comment import Comment
from flaskr.models.tag import Tag
from flaskr.extensions import db, photos


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
        title = request.form['title']
        body = request.form['body']
        tags = validate_tags(request.form['tags'])
        photo = request.files['photo']
        error = None

        if not tags:
            error = 'At least 1 tag is required.'
        if not body:
            error = 'Body is required.'
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # upload photo
            photo = upload_photo(photo) if photo else None
            # create post entry
            post = Post(title=title, body=body, author_id=g.user.id, image=photo)
            # add tmissing tags to db
            create_missing_tags(tags, all_tags)
            # add tags to post
            current_post_tags = Tag.get_tags_by_bodies(tags)
            for tag in current_post_tags:
                post.tags.append(tag)
            # save post
            post.save()
            return redirect(url_for('index'))

    return render_template('blog/create.html', tags=all_tags)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    all_tags = Tag.get_all_tags()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tags = validate_tags(request.form['tags'])
        photo = request.files['photo']
        remove_photo = request.form.getlist('remove_photo')
                                    
        error = None

        if not tags:
            error = 'At least 1 tag is required.'
        if not body:
            error = 'Body is required.'
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            post.image = update_photo(old_photo=post.image, new_photo=photo, remove_photo=remove_photo)
            create_missing_tags(tags, all_tags) # add new tags to the database.
            current_post_tags = Tag.get_tags_by_bodies(tags) # get tag objects with same body as selected.
            post.tags = []
            for tag in current_post_tags:
                post.tags.append(tag)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('blog/update.html', post=post, all_tags=all_tags)


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
        return tags 
    else:
        return False

def create_missing_tags(tags, all_tags):
    all_tags_contents = [tag.body for tag in all_tags]
    missing_tags = [tag for tag in tags if tag not in all_tags_contents]
    for tag_body in missing_tags:
        tag = Tag(body=tag_body)
        tag.save()

def upload_photo(photo):
    size = (399, 266)
    i = Image.open(photo)
    i = i.resize(size)
    filename = '{}.{}'.format(uuid.uuid4(), extension(photo.filename))

    i.save('/'.join([current_app.config['UPLOADED_PHOTOS_DEST'], filename]))
    return filename

def update_photo(old_photo, new_photo, remove_photo):
    if remove_photo:
        if old_photo:
            old_photo_path = '/'.join([current_app.config['UPLOADED_PHOTOS_DEST'], old_photo])
            try:
                os.remove(old_photo_path)
            except FileNotFoundError:
                pass
        return None
    if not new_photo or new_photo.filename is None:
        print('im hereee')
        return old_photo
    if old_photo:
        old_photo_path = '/'.join([current_app.config['UPLOADED_PHOTOS_DEST'], old_photo])
        try:
            os.remove(old_photo_path)
        except FileNotFoundError:
            pass
        
    return upload_photo(new_photo)