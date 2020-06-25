
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


