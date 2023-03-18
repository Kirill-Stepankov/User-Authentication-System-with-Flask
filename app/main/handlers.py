from app.main import bp
from flask_login import login_required, current_user
from flask import render_template
from app.main.forms import PostForm


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        pass
    return render_template('main/index.html', title='HAHAHA', form=form)
