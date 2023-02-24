import re
from flask import (
    Blueprint, render_template, request, flash
)
import feedparser

from flaskr.models.post import Post


bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/index', methods=('GET', 'POST')) 
def index():          

    page = request.args.get('page', 1, type=int)
    tag = request.args.get('tag')
    keyword = request.args.get('keyword')
    message = None

    if tag:
        message = tag
        posts = Post.get_posts_by_tag(tag=tag, page=page)
    elif keyword:
        message = keyword
        posts = Post.get_posts_by_phrase(keyword=keyword, page=page)
    else:
        posts = Post.get_all(page=page)
    
    if message and not posts.items:
        posts = Post.get_all(page=page)
        flash(f"Can't find posts matching criterium: '{message}'")
    feed = parse_and_feed_rss()
    return render_template('blog/index.html', posts=posts, keyword=message, post=feed)

def parse_and_feed_rss():
    FEEDURL = 'https://www.reddit.com/r/flask/new/.rss?sort=new'
    feed = feedparser.parse(FEEDURL)
    article = feed['entries'][0]
    body = re.search('<!-- SC_OFF -->(.*)<!-- SC_ON -->', article.get('content')[0]['value']).group(1)
    post = {
        'url': article.get('link'),
        'author': article.get('author').replace('/u/', ''),
        'created': article.get('updated'),
        'body': body
    }
    return post

