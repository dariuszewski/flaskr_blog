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

        # if request.args.get('keyword'):
        #     keyword = request.args['keyword']
        #     posts = Post.get_posts_by_phrase(keyword).all()
        #     if posts:
        #         return render_template('blog/index.html', posts=posts, keyword=keyword)
        #     else:
        #         message = f"Can't find posts matching criterium: '{keyword}'"
        #         flash(message)           

    
    page = request.args.get('page', 1, type=int)
    tag = request.args.get('tag')
    keyword = request.args.get('keyword')

    #TODO: do something with search without tag
    if tag:
        keyword = tag
        posts = Post.get_posts_by_tag(tag=tag, page=page)
    elif keyword:
        posts = Post.get_posts_by_phrase(keyword=keyword, page=page)
    else:
        posts = Post.get_all(page=page)

    return render_template('blog/index.html', posts=posts, keyword=keyword)
