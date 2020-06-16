from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField, DateField
from flaskblog.models import User, Order, Fish, Post, Comment, Mycarousel
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username         = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) # DataRequired means it cant be empty
    fullname         = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    address          = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=20)])
    email            = EmailField('Email', validators=[DataRequired(), Email()])
    password         = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #picture          = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit           = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('User Already Exists!')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email Already Exists!')

class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) # DataRequired means it cant be empty
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    address  = StringField('Address', validators=[DataRequired(), Length(min=2, max=20)])
    email    = EmailField('Email', validators=[DataRequired(), Email()])
    picture  = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'],'Images only!')])
    submit   = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user :
                raise ValidationError('User Already Exists!')
        

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email Already Exists!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit   = SubmitField('Login')

class PostForm(FlaskForm):
    title   = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], FileRequired())])
    submit  = SubmitField('Post')

class NewFishForm(FlaskForm):
    name        = StringField('Name', validators=[DataRequired()])
    picture     = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    price       = IntegerField('Price',validators=[DataRequired()])
    unit        = RadioField('Unit', validators=[DataRequired()], choices=[('kg','Kilograms(Kg)'),('g','Grams(g)')])
    size        = RadioField('Unit', validators=[DataRequired()], choices=[('Small','Small'),('Medium','Medium'),('Large','Large')])
    price_vatta = IntegerField('Price per Vatta')
    pc_vatta    = IntegerField('Piece per Vatta')
    isAvailable = BooleanField('The stock is currently available')
    submit      = SubmitField('Post Fish')

class OrderForm(FlaskForm):
    date_of_delivery = DateField(label='Please Select Date of Delivery', format='%Y-%m-%d', validators = [DataRequired('Please select Date of Delivery')])
    bargained_price  = IntegerField('Bargain Price')
    quantity         = IntegerField('Quantity')
    unit             = RadioField('Unit', validators=[DataRequired()], choices=[('kg','Kilograms(Kg)'),('g','Grams(g)'),('v','Vatta(Share)')])
    submit           = SubmitField('Order')

class BargainForm(FlaskForm):
    price  = IntegerField('Your Bargain Price',validators=[DataRequired()])
    submit = SubmitField('Bargain More')

class AcceptForm(FlaskForm):
    submit = SubmitField('Accept Order')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# I found the solution using format='%H:%M:%S.%f'


# time  =       TimeField       ('Enter the time HH:MM:SS.SSS   ', format='%H:%M:%S.%f', validators=[InputRequired()])

