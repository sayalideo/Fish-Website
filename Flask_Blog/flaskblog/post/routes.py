from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog.post.forms import PostForm
from flaskblog.post.utils import save_post_pic
from flaskblog.models import User, Post
from flaskblog import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if request.files['picture'] :
            picture_file = save_post_pic(form.picture.data)
        else:
            picture_file = 'waves.jpg'
            print('feels', picture_file)
        post = Post(title=form.title.data, content=form.content.data, post_author=current_user, image_file=picture_file, upvotes=0)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created !", 'success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html", form=form, legend="New Post")

@posts.route("/post/all", methods=['GET', 'POST'])
def all_posts():
    data = Post.query.all()
    return render_template('all_posts.html',data=data)

@posts.route('/post/<int:post_id>')
def post(post_id):
    # post = Post.query.get(post_id) can use get() as well
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    # post = Post.query.get(post_id) can use get() as well
    post = Post.query.get_or_404(post_id)
    if post.post_author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data :
            picture_file = save_post_pic(form.picture.data)
            current_user.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',form=form, legend="Update Post")

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    # post = Post.query.get(post_id) can use get() as well
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted!', 'success')
    return redirect(url_for('main.home'))


