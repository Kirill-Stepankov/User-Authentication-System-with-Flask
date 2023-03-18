from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError
from wtforms import SubmitField, StringField, EmailField, PasswordField, BooleanField
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("LogIn")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError("This username is already taken")

    def validate_email(self, email):
        if User.query.filter(User.email == email.data).first():
            raise ValidationError("This username is already taken")


class SendEmailResetPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Send")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("New password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat new password", validators=[EqualTo(password)])
