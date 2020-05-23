from flask import Flask, render_template

app = Flask(__name__, static_folder='')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/car-list-map')
def car_list_map():
    return render_template('car-list-map.html')


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


@app.route('/login-register')
def login_register():
    return render_template('login-register.html')


if __name__ == '__main__':
    app.run()
