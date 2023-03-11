from app.authentication import bp
from flask import render_template


@bp.route('/login')
def login():
    return render_template('auth/login.html', title='auth')
