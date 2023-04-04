from app.authentication import bp
from app.authentication.forms import LoginForm, RegistrationForm, SendEmailResetPasswordForm, ResetPasswordForm
from flask import render_template, session
from app.models import User
from app import db, app
from app.authentication.email import send_password_reset_email
from flask import flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from flask_babel import _


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='auth', form=form)


@bp.route('/registration', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(_('Registration completed!'))
        return redirect(url_for('auth.login'))

    return render_template('auth/registration.html', title='register', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/reset_request', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SendEmailResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        flash(_('The message has been sent. Check your email.'))
        if user is not None:
            send_password_reset_email(user)
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_request.html', form=form)


@bp.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect('auth.login')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Password has been reset'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
