import os
from flask import Flask, render_template, request, flash, redirect, url_for

from authentication import *
from forms import LoginForm, SignupForm, ForgotPassword, ResetPasswordForm, BookingForm
from dynamodb_operations import get_all_cars, rent_car
import requests as req
from user import User

app = Flask(__name__, static_folder='')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
logged_in_user = User()


@app.route('/')
def home():
    return render_template('index.html', msg=request.args.get('msg'))


@app.route('/login-register', methods=["GET", "POST"])
def login_register():
    loginform = LoginForm()
    signupform = SignupForm()
    forgotpasswordform = ForgotPassword()

    if forgotpasswordform.submit3.data and forgotpasswordform.validate_on_submit():
        result = request.form
        resp = forgotpassword(result['username'])
        if resp['success']:
            return redirect(url_for('confirm_forgot_password', msg="Check your email for the further procedure."))
        else:
            return render_template('login-register.html', loginform=LoginForm(), signupform=SignupForm(),
                                   forgotpasswordform=forgotpasswordform, loginmsg=resp['message'])

    if loginform.submit1.data and loginform.validate_on_submit():
        result = request.form
        resp = login(result['username'], result['password'])
        if resp['success']:
            logged_in_user.username = result['username']
            logged_in_user.token = resp['data']['access_token']
            return redirect(url_for('home', msg="You have successfully logged in."))
        else:
            return render_template('login-register.html', loginform=LoginForm(), signupform=SignupForm(),
                                   forgotpasswordform=forgotpasswordform, loginmsg=resp['message'])

    if signupform.submit2.data and signupform.validate_on_submit():
        result = request.form
        event = {
            'username': result['username'],
            'password': result['password'],
            'email': result['email'],
            'name': 'Atul',
        }
        resp = registration(event)
        if resp['success']:
            return redirect(url_for('home', msg=resp['message']))
        else:
            return render_template('login-register.html', loginform=LoginForm(), signupform=SignupForm(),
                                   forgotpasswordform=forgotpasswordform, signupmsg=resp['message'])
    return render_template('login-register.html', loginform=loginform, signupform=signupform,
                           forgotpasswordform=forgotpasswordform)


@app.route('/confirm-forgot-password', methods=["GET", "POST"])
def confirm_forgot_password():
    reset_password_form = ResetPasswordForm()
    if reset_password_form.submit4.data and reset_password_form.validate_on_submit():
        result = request.form
        event = {
            'username': result['username'],
            'password': result['password'],
            'code': result['ver_code']
        }
        resp = reset_password(event)
        if resp['success']:
            return redirect(url_for('home', msg="Password has been changed successfully."))
        else:
            return redirect(url_for('confirm_forgot_password', msg=resp['message']))
    return render_template('confirm-forgot-password.html', resetpasswordform=reset_password_form,
                           msg=request.args.get('msg'))


@app.route('/facebook-oauth')
def facebook_authentication():
    url = "https://rentcar..auth.us-east-1.amazoncognito.com/oauth2/authorize"
    param = {
        'identity_provider': 'facebook',
        'response_type': 'token',
        'client_id': CLIENT_ID,
        'redirect_uri': 'http:localhost:5000'
    }
    resp = req.get(url=url, params=param)
    return redirect(url_for('home', msg=resp))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/car-list-map')
def car_list_map():
    return render_template('car-list-map.html', message="Atul")


@app.route('/car-booking', methods=["GET", "POST"])
def car_booking():
    booking_form = BookingForm()
    if booking_form.submit5.data and booking_form.validate_on_submit():
        result1 = request.form
        resp = rent_car(result1)
        if resp['success']:
            return redirect(url_for('car_booking', bookingform=booking_form, msg=resp['message']))
        else:
            return redirect(url_for('car_booking', msg=resp['message']))
    return render_template('car-booking.html', bookingform=booking_form)


@app.route('/car-listing', methods=["GET", "POST"])
def car_listing():
    carslist = get_all_cars()
    return render_template('car-listing.html', carlist=carslist['Items'])


@app.route('/contact')
def contract():
    return render_template('contact.html')


@app.route('/drivers')
def drivers():
    return render_template('drivers.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/index-2')
def index_2():
    return render_template('index-2.html')


@app.route('/index-02')
def index_02():
    return render_template('index-02.html')


@app.route('/index-03')
def index_03():
    return render_template('index-03.html')


@app.route('/index-04')
def index_04():
    return render_template('index-04.html')


@app.route('/logout')
def sign_out():
    resp = logout(logged_in_user.token)
    return redirect(url_for('home', msg=resp['message']))


if __name__ == '__main__':
    app.run()
