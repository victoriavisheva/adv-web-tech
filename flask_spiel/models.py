#import database and user sesisons manager
from flask_spiel import db, login_manager
#import usermixin for managing user sessions
from flask_login import UserMixin

#reloading a user from the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#creating user class; columns - id(primary key in db), username, email, password and posts; specifying some attributes as unique and mandatory
#one to many relationships - user can create many ads; backref=author declares a new property on the Post class; lazy=true loads that data from db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#creating posts(ads) class;
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    pay = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.description}', '{self.date}', '{self.location}', '{self.pay}', '{self.contact}')"
