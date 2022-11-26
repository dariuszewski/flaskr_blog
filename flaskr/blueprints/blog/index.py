from flask import (
    Blueprint, render_template
)

from flaskr.models.post import Post


bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET',))
def index():
    posts = Post.get_all()
    return render_template('blog/index.html', posts=posts)