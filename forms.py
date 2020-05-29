from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit1 = SubmitField('Sign In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit2 = SubmitField('Sign Up Now')


class ForgotPassword(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit3 = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    ver_code = StringField('Verification Code', validators=[DataRequired()])
    submit4 = SubmitField('Reset')
