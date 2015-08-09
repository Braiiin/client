from datetime import datetime
from random import random
import functools
from client import hashing, login_manager
from client.exceptions import LogicException
from client.libs.core import User
from client.public.forms import LoginForm, RegisterForm
from flask import Blueprint, render_template, url_for, request, current_app
from flask_login import login_user, redirect, current_user, logout_user

# setup Blueprint
public = Blueprint('public', __name__)


def anonymous_required(f):
	"""Require anonymous - otherwise, redirect to private sphere"""
	@functools.wraps(f)
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated():
			return redirect(url_for('sphere.home'))
		return f(*args, **kwargs)
	return wrapper


@public.route('/')
def landing():
	"""Landing page"""
	return render_template('public/index.html')


@public.route('/login', methods=['POST', 'GET'])
@anonymous_required
def login():
	"""Login page"""
	try:
		form = LoginForm(request.form)
		user = User(username=form.username.data)
		if request.method == 'POST' and form.validate():
			user.get()
			nonce = hashing.hash_value(str(datetime.now()))
			password = hashing.hash_value(form.password.data, salt=user.salt)
			password = hashing.hash_value(password, salt=nonce)
			user.authenticate(password=password, nonce=nonce, salt=None)
			if user.get_id() and user.is_authenticated() and user.is_active():
				if login_user(user):
					return redirect(request.args.get('next') or url_for('sphere.home'))
			message = 'Login failed.'
	except LogicException as e:
		message = str(e)
	return render_template('public/login.html', **locals())


@public.route('/register', methods=['POST', 'GET'])
@anonymous_required
def register():
	"""Register page"""
	try:
		form = RegisterForm(request.form)
		if request.method == 'POST' and form.validate():
			salt = hashing.hash_value(str(datetime.now()))
			user = User(
				name=form.name.data,
				email=form.email.data,
				password=hashing.hash_value(form.password.data, salt=salt),
			    salt=salt,
			    username=form.username.data
			).create()
			if login_user(user):
				return redirect(url_for('sphere.home'))
			else:
				return redirect(url_for('public.login'))
	except LogicException as e:
		message = str(e)
	return render_template('public/register.html', **locals())


@login_manager.user_loader
def load_user(userId):
	"""Loading a user from saved userId"""
	user = User(id=userId).get()
	if user.is_active():
		return user
	else:
		return None


@login_manager.unauthorized_handler
def unauthorized():
	"""Where unauthenticated users are sent"""
	return redirect(url_for('public.login'))


@public.route('/logout')
def logout():
	"""Logout the user"""
	logout_user()
	return redirect(url_for('public.login'))