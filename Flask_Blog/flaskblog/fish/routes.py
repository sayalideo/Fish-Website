from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog.fish.forms import NewFishForm, OrderForm, BargainForm, AcceptForm
from flaskblog.models import User, Order, Fish
from flaskblog import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flaskblog.fish.utils import save_fish_pic
from datetime import datetime

fishes = Blueprint('fishes', __name__)

@fishes.route("/fish/new", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template("create_fish.html", form=form, legend="New Post")

@fishes.route("/fish/all", methods=['GET', 'POST'])
def all_fish():
    page = request.args.get('page', 1, type=int)
    data = Fish.query.order_by(Fish.upload_date.desc()).paginate(page=page, per_page=12)
    return render_template('all_fish.html',data=data)

@fishes.route("/order/new", methods=['GET', 'POST'])
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
        return redirect(url_for('fishes.order', order=order.id))
    return render_template("create_order.html", form=form, buyer=buyer, seller=seller, d=fish)

@fishes.route("/order", methods=['GET', 'POST'])
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
        return redirect(url_for('fishes.order', order=order.id))
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

@fishes.route("/accept", methods=['POST'])
@login_required
def accept():
    order  = Order.query.filter_by(id=request.args.get('order')).first()
    order.is_valid = True
    db.session.commit()
    flash('Your Order has been accepted!', 'success')
    return redirect(url_for('fishes.order', order=order.id))

@fishes.route("/cart", methods=['GET'])
@login_required
def cart():
    orders = Order.query.filter_by(buyer_id=current_user.id).all() 
    return render_template('all_orders.html',orders=orders, user='buyer')


@fishes.route("/all_orders", methods=['GET'])
@login_required
def all_orders():
    orders = Order.query.filter_by(seller_id=current_user.id).all() 
    return render_template('all_orders.html',orders=orders, user='seller')

