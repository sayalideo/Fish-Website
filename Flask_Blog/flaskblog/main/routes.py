
from flask import render_template
from flaskblog.models import Post
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    data = Post.query.all()
    return render_template('home.html',data=data)

@main.route("/about")
def about():
    return render_template('about.html')


