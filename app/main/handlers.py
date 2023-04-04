from app.main import bp
from flask_login import login_required, current_user
from flask import render_template
from app.main.forms import PostForm
from app.models import Post
from app import db, app
from flask import redirect, url_for, request


@bp.route('/index', methods=['POST', 'GET'])
@bp.route('/', methods=['POST', 'GET'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("main/index.html", title='Main', posts=posts.items, form=form,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/change_lan')
@login_required
def change_language():
    current_user.language = 'ru' if current_user.language == 'en' else 'en'
    db.session.commit()
    return redirect(request.referrer)
