from app.oauth import bp
from flask import url_for, render_template, redirect, flash
from app import oauth, db
from app.models import User
from flask_login import current_user, login_user
from flask_babel import _

@bp.route('/google/login')
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    redirect_uri = url_for('oauth.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@bp.route('/google/callback')
def google_authorize():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    token = oauth.google.authorize_access_token()

    user_login = token['userinfo']['name']
    user_email = token['userinfo']['email']
    locale = 'ru' if token['userinfo']['locale'] == 'ru' else 'en'

    user_by_email = User.query.filter(User.email == user_email).first()

    if user_by_email is None:
        new_user = User(username=user_login, email=user_email, language=locale)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
    elif user_by_email.password_hash is not None:
        flash(_('A user with such an email already exists in the application. Please, log in to the account.'))
        return redirect(url_for('auth.login'))
    else:
        login_user(user_by_email)
        
    return redirect(url_for('main.index'))


@bp.route('/github/login')
def github_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    redirect_uri = url_for('oauth.github_authorize', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@bp.route('/github/callback')
def github_authorize():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    token = oauth.github.authorize_access_token()
    email_resp = oauth.github.get('user/emails', token=token)
    user_resp = oauth.github.get('user', token=token)

    user_resp.raise_for_status()
    email_resp.raise_for_status()

    emails = email_resp.json()
    user = user_resp.json()

    user_login = user['login']
    user_email = emails[0]['email']

    user_by_email = User.query.filter(User.email == user_email).first()

    if user_by_email is None:
        new_user = User(username=user_login, email=user_email)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
    elif user_by_email.password_hash is not None:
        flash(_('A user with such an email already exists in the application. Please, log in to the account.'))
        return redirect(url_for('auth.login'))
    else:
        login_user(user_by_email)
        
    return redirect(url_for('main.index'))

