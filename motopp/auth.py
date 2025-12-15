from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
import logging

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login() -> str:
    """
    Render the login page.

    :return: Rendered login page.
    """
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post() -> str:
    """
    Handle the login POST request. The user is authenticated with email and password.

    :return: Redirect to user's bikes page on successful login, else back to login page.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    logging.info(f"User logged in: {user.name}")
    return redirect(url_for('main.mybikes'))


@auth.route('/signup')
def signup() -> str:
    """
    Render the signup page.

    :return: Rendered signup page.
    """
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post() -> str:
    """
    Handle the signup POST request. The user is registered with email, name and password.

    :return: Redirect to login page on successful registration, else back to signup page.
    """
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()
    logging.info(f"User created: {new_user.name}")
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout() -> str:
    """
    Logout the currently logged in user.

    :return: Redirect to the index page after logout.
    """
    logout_user()
    return redirect(url_for('main.index'))
