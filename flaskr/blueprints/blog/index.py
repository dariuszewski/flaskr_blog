from flask import (
    Blueprint, render_template, request, flash
)

from flaskr.models.post import Post


bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST')) 
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        posts = Post.get_posts_by_phrase(keyword).all()
        if posts:
            return render_template('blog/index.html', posts=posts, keyword=keyword)
        else:
            message = f"Can't find posts matching criterium: '{keyword}'"
            flash(message)
            
    posts = Post.get_all()
    if request.args:
        print('AM I HERE???')
        searched_tag = request.args['tag']
        filtered_posts = []
        for post in posts:
            for post_tag in post.tags:
                if searched_tag == post_tag.body:
                    filtered_posts.append(post)
        posts = list(set(filtered_posts))
        return render_template('blog/index.html', posts=posts, keyword=searched_tag)

    return render_template('blog/index.html', posts=posts, keyword=None)
