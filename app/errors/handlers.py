from app.errors import bp
from flask import render_template
from app import db, app


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', app=app), 404


@bp.app_errorhandler(500)
def page_not_found(e):
    db.session.rollback()
    return render_template('errors/500.html', app=app), 500
