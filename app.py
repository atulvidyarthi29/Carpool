import os
import time
from flask import Flask, render_template, request, redirect, url_for

from authentication import *
from forms import LoginForm, SignupForm, ForgotPassword, ResetPasswordForm, BookingForm
from dynamodb_operations import *
import requests as req
from user import User
from datetime import datetime

app = Flask(__name__, static_folder='')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
logged_in_user = User()


@app.route('/')
def home():
    return render_template('index.html', msg=request.args.get('msg'), user=logged_in_user)


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
                                   forgotpasswordform=forgotpasswordform, loginmsg=resp['message'], user=logged_in_user)

    if loginform.submit1.data and loginform.validate_on_submit():
        result = request.form
        resp = login(result['username'], result['password'])
        if resp['success']:
            logged_in_user.username = result['username']
            logged_in_user.token = resp['data']['access_token']
            return redirect(url_for('home', msg="You have successfully logged in."))
        else:
            return render_template('login-register.html', loginform=LoginForm(), signupform=SignupForm(),
                                   forgotpasswordform=forgotpasswordform, loginmsg=resp['message'], user=logged_in_user)

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
                                   forgotpasswordform=forgotpasswordform, signupmsg=resp['message'],
                                   user=logged_in_user)
    return render_template('login-register.html', loginform=loginform, signupform=signupform,
                           forgotpasswordform=forgotpasswordform, user=logged_in_user)


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
                           msg=request.args.get('msg'), user=logged_in_user)


@app.route('/facebook-oauth')
def facebook_authentication():
    url = "https://rentcar.auth.us-east-1.amazoncognito.com/login"
    param = {
        'client_id': CLIENT_ID,
        'response_type': 'token',
        'scope': ['email', 'openid', 'profile'],
        'redirect_uri': 'https://jyi75vyoma.execute-api.us-east-1.amazonaws.com/dev/'
    }
    resp = req.get(url=url, params=param)
    return redirect(url_for('home', msg=resp))


@app.route('/car-booking/<int:item_id>', methods=["GET", "POST"])
def car_booking(item_id):
    car = get_car(item_id)['Item']
    car['carid'] = int(car['carid'])
    booking_form = BookingForm()
    if booking_form.submit5.data and booking_form.validate_on_submit():
        if logged_in_user.username == '':
            return redirect(url_for('car_booking', item_id=item_id, msg="You must login first!"))
        result1 = request.form
        event = {
            'id': int(time.time()),
            'place': result1['place'],
            'pickup_date': result1['pick_up_date'],
            'days': result1['days'],
            'order_date': str(datetime.today()),
            'carid': car,
            'payment_type': "Cheque",
            'username': logged_in_user.username,
        }
        resp = rent_car(event)
        if resp['success']:
            return redirect(url_for('past_bookings', msg=resp['message']))
        else:
            return redirect(url_for('past_bookings', msg=resp['message']))
    return render_template('car-booking.html', bookingform=booking_form, user=logged_in_user, car=car,
                           msg=request.args.get('msg'))


@app.route('/past-bookings', methods=["GET", "POST", ])
def past_bookings():
    bookings = get_bookings(logged_in_user.username)
    return render_template('car-booked-list.html', user=logged_in_user, bookings=bookings)


@app.route('/delete/<int:item_id>')
def delete_button(item_id):
    resp = delete_booking(item_id)
    print(resp)
    return redirect(url_for('past_bookings'))


@app.route('/car-listing', methods=["GET", "POST"])
def car_listing():
    carslist = get_all_cars()
    return render_template('car-listing.html', carlist=carslist['Items'], user=logged_in_user)


@app.route('/logout')
def sign_out():
    resp = logout(logged_in_user.token)
    logged_in_user.username = ""
    logged_in_user.token = ""
    return redirect(url_for('home', msg=resp['message']))


@app.route('/about')
def about():
    return render_template('about.html', user=logged_in_user)


@app.route('/car-list-map')
def car_list_map():
    return render_template('car-list-map.html', user=logged_in_user)


@app.route('/contact')
def contact():
    return render_template('contact.html', user=logged_in_user)


@app.route('/drivers')
def drivers():
    return render_template('drivers.html', user=logged_in_user)


@app.route('/faq')
def faq():
    return render_template('faq.html', user=logged_in_user)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html', user=logged_in_user)


@app.route('/index-2')
def index_2():
    return render_template('index-2.html', user=logged_in_user)


@app.route('/index-02')
def index_02():
    return render_template('index-02.html', user=logged_in_user)


@app.route('/index-03')
def index_03():
    return render_template('index-03.html', user=logged_in_user)


@app.route('/index-04')
def index_04():
    return render_template('index-04.html', user=logged_in_user)


if __name__ == '__main__':
    app.run()
