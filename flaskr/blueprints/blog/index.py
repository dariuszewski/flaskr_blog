from flask import (
    Blueprint, render_template, request, flash
)

from flaskr.models.post import Post


bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST')) 
def index():          

    if request.args:

        if request.args.get('keyword') and request.args.get('tag'):
            # This scenario can happen only if user will type params in the url
            searched_tag = request.args['tag']
            keyword = request.args['keyword']
            posts = Post.get_posts_by_tag_and_filter_by_keyword(searched_tag, keyword)
            if posts:
                title = f'{searched_tag} with text search for {keyword}'
                return render_template('blog/index.html', posts=posts, keyword=title)
            else:
                message = f"Can't find posts with tag '{searched_tag}' and containing '{keyword}' phrase."
                flash(message)
                posts = Post.get_all()
                return render_template('blog/index.html', posts=posts)

        if request.args.get('keyword'):
            keyword = request.args['keyword']
            posts = Post.get_posts_by_phrase(keyword).all()
            if posts:
                return render_template('blog/index.html', posts=posts, keyword=keyword)
            else:
                message = f"Can't find posts matching criterium: '{keyword}'"
                flash(message)
            
        if request.args.get('tag'):
            searched_tag = request.args['tag']
            posts = Post.get_posts_by_tag(searched_tag).all()
            if posts:
                return render_template('blog/index.html', posts=posts, keyword=searched_tag)
            else:
                message = f"Can't find posts matching criterium: '{searched_tag}'"
                flash(message)              

    posts = Post.get_all()
    return render_template('blog/index.html', posts=posts)
