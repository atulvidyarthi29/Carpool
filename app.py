import os
from flask import Flask, render_template, request, flash, redirect, url_for

from authentication import login, registration
from forms import LoginForm, SignupForm

app = Flask(__name__, static_folder='')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

username = None


@app.route('/')
def home():
    return render_template('index.html', msg=request.args.get('msg'))


@app.route('/login-register', methods=["GET", "POST"])
def login_register():
    loginform = LoginForm()
    signupform = SignupForm()

    if loginform.submit1.data and loginform.validate_on_submit():
        result = request.form
        resp = login(result['username'], result['password'])
        if resp['success']:
            username = result['username']
            return redirect(url_for('home', msg="You have successfully logged in."))
        else:
            return render_template('login-register.html', loginform=LoginForm(), signupform=SignupForm(),
                                   loginmsg=resp['message'])

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
            username = result['username']
            return redirect(url_for('home', msg=resp['message']))
        else:
            return render_template('login-register.html', loginform=LoginForm(), signupform=SignupForm(),
                                   signupmsg=resp['message'])
    return render_template('login-register.html', loginform=loginform, signupform=signupform)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/car-list-map')
def car_list_map():
    return render_template('car-list-map.html', message="Atul")


@app.route('/car-booking')
def car_booking():
    return render_template('car-booking.html')


@app.route('/car-listing')
def car_listing():
    return render_template('car-listing.html')


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


if __name__ == '__main__':
    app.run()
