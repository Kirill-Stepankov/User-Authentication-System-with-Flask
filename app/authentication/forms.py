from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError
from wtforms import SubmitField, StringField, EmailField, PasswordField, BooleanField
from app.models import User
from flask_babel import lazy_gettext as _l
from flask_babel import _


class LoginForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember = BooleanField(_l("Remember me"))
    submit = SubmitField(_l("LogIn"))


class RegistrationForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    email = EmailField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    repeat_password = PasswordField(_l("Repeat password"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l("Register"))

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError(_("This username is already taken"))

    def validate_email(self, email):
        if User.query.filter(User.email == email.data).first():
            raise ValidationError(_("This username is already taken"))


class SendEmailResetPasswordForm(FlaskForm):
    email = EmailField(_l("Email"), validators=[DataRequired()])
    submit = SubmitField(_l("Send"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("New password"), validators=[DataRequired()])
    repeat_password = PasswordField(_l("Repeat new password"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l("Reset"))
