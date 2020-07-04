from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog.user.forms import RegistrationForm, LoginForm, UpdateForm, EmptyForm, RequestResetForm, ResetPasswordForm
from flaskblog.user.utils import save_picture, send_reset_email
from flaskblog.models import User, Order, Fish, Post, Comment, Mycarousel
from flaskblog import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, fullname = form.fullname.data, address=form.address.data, email=form.email.data, password=hashed_password, points=0)
        db.session.add(user)
        db.session.commit()
        name = form.fullname.data
        s    = 'Account created for ' + name + ' successfully !'
        flash(s,'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.','danger')
    return render_template('login.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.address.data = current_user.address
        form.email.data = current_user.email
        points         = current_user.points
    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', img_file=img_file, form=form, points=points)

@users.route('/user/<string:username>')
@login_required
def user_popup(username):
    form = EmptyForm() 
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    data = Fish.query.filter_by(fish_seller=user).order_by(Fish.upload_date.desc()).paginate(page=page, per_page=3)
    posts = Post.query.filter_by(post_author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user.html', user=user, form=form, data=data, posts=posts)

@users.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('users.user_popup', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('users.user_popup', username=username))
    else:
        return redirect(url_for('main.home'))


@users.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('users.user_popup', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('users.user_popup', username=username))
    else:
        return redirect(url_for('main.home'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent for resetting password!', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html',form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is expired!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        name = form.fullname.data
        s    = 'Password has been updated! ' + name + ' successfully !'
        flash(s,'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)