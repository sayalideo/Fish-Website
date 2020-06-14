from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# subs = db.Table('subs',
#     db.Column('buyer_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('seller_id', db.Integer, db.ForeignKey('user.id')),
#     db.relationship("User", foreign_keys=['user.id']),
#     db.relationship("User", foreign_keys=['user.id'])
# )

ords = db.Table('ords',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('fish_id', db.Integer, db.ForeignKey('fish.id'))
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
class User(db.Model, UserMixin):
    id            = db.Column(db.Integer, primary_key = True)
    username      = db.Column(db.String(20), unique=True, nullable=False)
    fullname      = db.Column(db.String(50))
    email         = db.Column(db.String(20), unique=True)
    address       = db.Column(db.String(120))
    image_file    = db.Column(db.String(20), nullable=False, default='default.jpg')
    password      = db.Column(db.String(60), nullable=False)
    points        = db.Column(db.Integer)
    #cart          = db.relationship('Order', backref='buyer', lazy='dynamic')
    #subscriptions = db.relationship('User', secondary=subs, backref=db.backref('subscribers'), lazy='dynamic')
    posts         = db.relationship('Post', backref='post_author', lazy=True)
    fishes        = db.relationship('Fish', backref='fish_seller', lazy='dynamic')
    #orders        = db.relationship('Order', backref='order_seller', lazy='dynamic')
    mycarousel    = db.relationship('Mycarousel', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Fish.query.join(
            followers, (followers.c.followed_id == Fish.seller_id)).filter(
                followers.c.follower_id == self.id)
        own = Fish.query.filter_by(seller_id=self.id)
        return followed.union(own).order_by(Fish.upload_date.desc())
    #username='hh', fullname='Haresh Hambire', email='haresh@gmail.com', password='qwe', points=0
    #username='sharad', fullname='Sharad Chaudhary', email='sharad@gmail.com', password='qwe', points=0
    #username='saiy', fullname='Sayali Deo', email='saiy@gmail.com', password='qwe', points=0
# class Cart(db.Model):
#     id     = db.Column(db.Integer, primary_key = True)
#     seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
#     seller = db.relationship("User", foreign_keys=[seller_id])
#     order = db.relationship("Order", foreign_keys=[order_id])

class Order(db.Model):
    id               = db.Column(db.Integer, primary_key = True)
    date_placed      = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    date_of_delivery = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    bargained_price  = db.Column(db.Integer)
    quantity         = db.Column(db.Integer)
    unit             = db.Column(db.String(20), nullable=False) # kg,gm,pc
    is_valid         = db.Column(db.Boolean, nullable=False, default=False)
    seller_id        = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller           = db.relationship("User", foreign_keys=[seller_id])
    buyer            = db.relationship("User", foreign_keys=[buyer_id])

    def __repr__(self):
        return f"Order('{self.title}', '{self.date_placed}', '{self.date_of_delivery}', '{self.bargained_price}')"

class Fish(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    image_file  = db.Column(db.String(20), nullable=False)
    price       = db.Column(db.Integer, nullable=False)
    unit        = db.Column(db.String(20), nullable=False) # kg,gm,pc
    isAvailable = db.Column(db.Boolean, nullable=False, default=False)
    orders      = db.relationship('Order', secondary=ords, backref=db.backref('fishes'), lazy='dynamic')
    seller_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Fish('{self.name}', '{self.price}', '{self.isAvailable}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20))
    upvotes = db.Column(db.Integer)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='mypost', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    upvotes     = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Comment('{self.description}', '{self.date_posted}', '{self.post_id}')"

class Mycarousel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image_file = db.Column(db.String(20),nullable=False, default='carousel/boats.jpg')
    description = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.description}', '{self.date_posted}')"


'''
from flaskblog import db
db.create_all()
from flaskblog.models import Seller
s1 = User(username='hh', fullname='Haresh Hambire', email='haresh@gmail.com', address='Mahim',password='qwe', points=0)
db.session.add(s1)
db.session.commit()
Seller.query.all()
Seller.query.filter_by(username='hh').all() ... returns list
Seller.query.filter_by(username='hh').first() ... returns single item


u2.followed.append(u1)
>>> u1.followers
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x7f58877ea470>
>>> u1.followers.username
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'AppenderBaseQuery' object has no attribute 'username'
>>> u1.followers[0].username
'sharad'
>>> 
'''