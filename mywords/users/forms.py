from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
	email = StringField("Email address", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")
	register = SubmitField("Register")


class RegisterForm(FlaskForm):
	first_name = StringField("First name", validators=[DataRequired()])
	last_name = StringField("Last name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message='Passwords Must Match!')])
	confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
	submit = SubmitField("Register")