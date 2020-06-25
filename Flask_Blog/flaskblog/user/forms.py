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

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Please Enter the email registered with this account')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# I found the solution using format='%H:%M:%S.%f'


# time  =       TimeField       ('Enter the time HH:MM:SS.SSS   ', format='%H:%M:%S.%f', validators=[InputRequired()])

