from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, RadioField
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


class BookingForm(FlaskForm):
    place = TextAreaField(
        'pickup_address', validators=[DataRequired()])
    pick_up_date = StringField(
        'date_pickup', validators=[DataRequired()])
    days = StringField('car_type', validators=[DataRequired()])
    # payment_type = RadioField('payment_type', choices=[
    #     'Direct bank Transfer', 'Cheque Payment', 'Credit Card', 'Paypal'])
    submit5 = SubmitField('Book Now')


class CarListingForm(FlaskForm):
    carcompany = StringField('carcompany', validators=[DataRequired()])
    cartype = StringField('cartype', validators=[DataRequired()])
