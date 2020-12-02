#import of os and secrets for secret key/user sessions
import os
import secrets
#import of render template method, url_for to handle dynamic urls, flash messages, redirects, request for post and get requests, abort function
from flask import render_template, url_for, flash, redirect, request, abort
#import of app,db, bryptt from flask_spiel folder
from flask_spiel import app, db, bcrypt
#import forms from forms.py
from flask_spiel.forms import RegistrationForm, LoginForm, PostForm
#import the teo databse models (tables) from models.py
from flask_spiel.models import User, Post
#import user sesison managing extensions
from flask_login import login_user, current_user, logout_user, login_required

#defining functions that render sepcific page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/ads")
@login_required
def ads():
    posts = Post.query.all()
    return render_template('ads.html', posts=posts)


@app.route("/monologues")
def monologues():
    return render_template('monologues.html', title='Monologues')


@app.route("/tips")
def tips():
    return render_template('tips.html', title='Tips')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('ads'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ads'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('ads'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, date=form.date.data, location=form.location.data, pay=form.pay.data, contact=form.contact.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('ads'))
    return render_template('create_post.html', title='New Post',
                           form=form)


