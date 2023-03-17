from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, EqualTo
from wtforms import SubmitField, StringField, EmailField, PasswordField


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("LogIn")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat password", validators=[EqualTo(password)])
    submit = SubmitField("Register")


class SendEmailResetPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Send")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("New password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat new password", validators=[EqualTo(password)])
