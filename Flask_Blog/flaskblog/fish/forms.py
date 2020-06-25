from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class NewFishForm(FlaskForm):
    name        = StringField('Name', validators=[DataRequired()])
    picture     = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    price       = IntegerField('Price',validators=[DataRequired()])
    unit        = RadioField('Unit', validators=[DataRequired()], choices=[('kg','Kilograms(Kg)'),('g','Grams(g)')])
    size        = RadioField('Size', validators=[DataRequired()], choices=[('Small','Small'),('Medium','Medium'),('Large','Large')])
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

