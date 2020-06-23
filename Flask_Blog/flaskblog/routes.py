
import os
import secrets
from datetime import datetime
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateForm, PostForm, NewFishForm, EmptyForm, OrderForm, BargainForm, AcceptForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Order, Fish, Post, Comment, Mycarousel
from flaskblog import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    data = Post.query.all()
    return render_template('home.html',data=data)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, fullname = form.fullname.data, address=form.address.data, email=form.email.data, password=hashed_password, points=0)
        db.session.add(user)
        db.session.commit()
        name = form.fullname.data
        s    = 'Account created for ' + name + ' successfully !'
        flash(s,'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.','danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex   = secrets.token_hex(8)
    _, f_ext     = os.path.splitext(form_picture.filename)
    picture_fn   = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size  = (256,256)
    i            = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data :
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email    = form.email.data
        current_user.address  = form.address.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.address.data = current_user.address
        form.email.data = current_user.email
        points         = current_user.points
    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', img_file=img_file, form=form, points=points)

def save_fish_pic(form_picture):
    random_hex   = secrets.token_hex(8)
    _, f_ext     = os.path.splitext(form_picture.filename)
    picture_fn   = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/fish_pics', picture_fn)
    output_size  = (256,256)
    i            = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/fish/new", methods=['GET', 'POST'])
@login_required
def new_fish():
    form = NewFishForm()
    if form.is_submitted():
        picture_file = save_fish_pic(form.picture.data)
        if form.picture.data :
            picture_file = save_fish_pic(form.picture.data)
        else:
            picture_file = 'icon.jpeg' 
        fish = Fish(name=form.name.data, price=form.price.data, unit=form.unit.data, size=form.size.data, image_file=picture_file, pc_vatta=form.pc_vatta.data, price_vatta=form.price_vatta.data, isAvailable=form.isAvailable.data, fish_seller=current_user)
        db.session.add(fish)
        db.session.commit()
        flash("Your Fish has been created !", 'success')
        return redirect(url_for('home'))
    return render_template("create_fish.html", form=form, legend="New Post")

@app.route("/fish/all", methods=['GET', 'POST'])
def all_fish():
    page = request.args.get('page', 1, type=int)
    data = Fish.query.order_by(Fish.upload_date.desc()).paginate(page=page, per_page=12)
    return render_template('all_fish.html',data=data)

def save_post_pic(form_picture):
    random_hex   = secrets.token_hex(8)
    _, f_ext     = os.path.splitext(form_picture.filename)
    picture_fn   = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)
    output_size  = (1920,1080)
    i            = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if request.files['picture'] :
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = 'waves.jpg'
            print('feels', picture_file)
        post = Post(title=form.title.data, content=form.content.data, post_author=current_user, image_file=picture_file, upvotes=0)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created !", 'success')
        return redirect(url_for('home'))
    return render_template("create_post.html", form=form, legend="New Post")

@app.route("/post/all", methods=['GET', 'POST'])
def all_posts():
    data = Post.query.all()
    return render_template('all_posts.html',data=data)

@app.route('/post/<int:post_id>')
def post(post_id):
    # post = Post.query.get(post_id) can use get() as well
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    # post = Post.query.get(post_id) can use get() as well
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',form=form, legend="Update Post")

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    # post = Post.query.get(post_id) can use get() as well
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
@login_required
def user_popup(username):
    form = EmptyForm() 
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    data = Fish.query.filter_by(fish_seller=user).order_by(Fish.upload_date.desc()).paginate(page=page, per_page=12)
    return render_template('user.html', user=user, form=form, data=data)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('home'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user_popup', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user_popup', username=username))
    else:
        return redirect(url_for('home'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('home'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user_popup', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user_popup', username=username))
    else:
        return redirect(url_for('home'))

@app.route("/order/new", methods=['GET', 'POST'])
@login_required
def new_order():
    buyer  = User.query.filter_by(username=request.args.get('buyername')).first()
    seller = User.query.filter_by(username=request.args.get('sellername')).first()
    fish   = Fish.query.filter_by(id=request.args.get('fish')).first()
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(date_of_delivery=form.date_of_delivery.data, bargained_price=form.bargained_price.data, quantity=form.quantity.data, unit=form.unit.data, seller_id=seller.id, buyer_id=buyer.id, last_modified_by=buyer.username)
        order.fishes.append(fish)
        db.session.add(order)
        db.session.commit()
        flash("Your Order has been placed !", 'success')
        return redirect(url_for('order', order=order.id))
    return render_template("create_order.html", form=form, buyer=buyer, seller=seller, d=fish)

@app.route("/order", methods=['GET', 'POST'])
@login_required
def order():
    order  = Order.query.filter_by(id=request.args.get('order')).first()
    fish   = order.fishes[0]
    form   = BargainForm() 
    accept = AcceptForm()
    if form.validate_on_submit():
        order.bargained_price  = form.price.data
        order.last_modified_by = current_user.username
        order.last_modified_on = datetime.utcnow()
        db.session.commit()
        flash('Your Bargain has been updated!', 'success')
        return redirect(url_for('order', order=order.id))
    if order.is_valid:
        bill = order.bargained_price*order.quantity
    else:
        if order.unit == fish.unit:
            bill = fish.price*order.quantity
        elif order.unit == 'kg' and fish.unit == 'g':
            bill = fish.price*order.quantity*1000
        elif order.unit == 'g' and fish.unit == 'kg':
            bill = fish.price*order.quantity/1000
        elif order.unit == 'v':
            bill = fish.price_vatta*order.quantity 
          
    return render_template("myorder.html", order=order, d=fish, bill=bill, form=form, accept=accept)

@app.route("/accept", methods=['POST'])
@login_required
def accept():
    order  = Order.query.filter_by(id=request.args.get('order')).first()
    order.is_valid = True
    db.session.commit()
    flash('Your Order has been accepted!', 'success')
    return redirect(url_for('order', order=order.id))

@app.route("/cart", methods=['GET'])
@login_required
def cart():
    orders = Order.query.filter_by(buyer_id=current_user.id).all() 
    return render_template('all_orders.html',orders=orders, user='buyer')


@app.route("/all_orders", methods=['GET'])
@login_required
def all_orders():
    orders = Order.query.filter_by(seller_id=current_user.id).all() 
    return render_template('all_orders.html',orders=orders, user='seller')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Request Message', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To Reset your password, visit the following link :\n {url_for('reset_token', token=token, _external=True)}\nIf you did not request this email, please ignore it and no changes shall be saved'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent for resetting password!', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html',form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is expired!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        name = form.fullname.data
        s    = 'Password has been updated! ' + name + ' successfully !'
        flash(s,'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)