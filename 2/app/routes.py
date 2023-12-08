from flask import render_template, redirect, url_for, flash
from flask import request
from app import app, db
from app.models import Product, Review, User    
from app.forms import ReviewForm, ProductForm
from flask_bcrypt import Bcrypt
from flask_login import login_required, current_user, login_user, logout_user
#limiter
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
#qr code
from app.utils import generate_totp_secret, generate_qr_code_uri, verify_totp
import pyotp

limiter = Limiter(
    key_func=lambda: current_user.get_id() if current_user.is_authenticated else request.remote_addr,
    app=app
)


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products, current_user=current_user)


@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(content=form.content.data, product=product)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('product', product_id=product_id))

    return render_template('product.html', product=product, form=form)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_product.html', form=form)

#oppgave3

bcrypt = Bcrypt(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
     

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
      
        totp_secret = generate_totp_secret()

        new_user = User(username=username, email=email, password=hashed_password, totp_secret=totp_secret)
        db.session.add(new_user)
       
        db.session.commit()

        flash('Your user has been created.', 'success')

        # qr ciode generating
        totp_uri = generate_qr_code_uri(username, totp_secret)

        return redirect(url_for('setup_2fa', username=username, totp_uri=totp_uri))
    return render_template('register.html')  

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("3 per 1 minute") 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        totp_code = request.form['totp_code'] 


        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            if user.totp_secret:
                totp = pyotp.TOTP(user.totp_secret)
                if totp.verify(totp_code):
                   
                    login_user(user, remember=True)
                    flash('Login success!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Wrong TOTP code.', 'danger')
            else:
                flash('TOTP secret not found for the user.', 'danger')
        else:
            flash('Login unsuccessful.', 'danger')


    return render_template('login.html')  

#logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

#user page route

@app.route('/user')
@login_required
def user():
    print(current_user)
    app.logger.debug(current_user)

    return render_template('user.html', user=current_user)

@app.route('/setup_2fa/<username>')
def setup_2fa(username):
    totp_uri = request.args.get('totp_uri')

    user = User.query.filter_by(username=username).first()

    if user:
        return render_template('setup_2fa.html', totp_uri=totp_uri)

    flash('User not found', 'danger')
    return redirect(url_for('index'))