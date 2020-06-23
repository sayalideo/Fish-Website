from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = '48b95e763384fd9a92ff9bd0111f0b18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes