from flask import (
    Blueprint, render_template, request
)

from flaskr.models.post import Post


bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST')) 
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        posts = Post.get_posts_by_phrase(keyword)
        return render_template('blog/index.html', posts=posts)

    posts = Post.get_all()
    if request.args:
        searched_tag = request.args['tag']
        filtered_posts = []
        for post in posts:
            for post_tag in post.tags:
                if searched_tag == post_tag.body:
                    filtered_posts.append(post)
        posts = list(set(filtered_posts))
        return render_template('blog/index.html', posts=posts, searched_tag=searched_tag)

    return render_template('blog/index.html', posts=posts)
