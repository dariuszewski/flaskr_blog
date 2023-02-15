from flask import (
    Blueprint, render_template, request, flash
)

from flaskr.models.post import Post


bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST')) 
def index():          

    page = request.args.get('page', 1, type=int)
    tag = request.args.get('tag')
    keyword = request.args.get('keyword')
    message = None
    
    if tag or keyword:
        if tag:
            message = tag
            posts = Post.get_posts_by_tag(tag=tag, page=page)
        if keyword:
            message = keyword
            posts = Post.get_posts_by_phrase(keyword=keyword, page=page)
        if not posts.items:
            posts = Post.get_all(page=page)
            flash(f"Can't find posts matching criterium: '{keyword}'")           
    else:
        posts = Post.get_all(page=page)

    return render_template('blog/index.html', posts=posts, keyword=message)
