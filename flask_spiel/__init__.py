#flask import
from flask import Flask
#database import
from flask_sqlalchemy import SQLAlchemy
#bcrypt for password hashing import
from flask_bcrypt import Bcrypt
#sessions manager import
from flask_login import LoginManager

#instantiating the flask app
app = Flask(__name__)
#secret key generated for user sessions
app.config['SECRET_KEY'] = '936599346d98434cbb08eb6d9244e455'
#configuration of database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#bcrypt confriguration
bcrypt = Bcrypt(app)
#user session configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#importing routes file
from flask_spiel import routes