from app import bcrypt
from app.lib.core import User
from app.public.forms import LoginForm, RegisterForm
from flask import Blueprint, render_template, url_for, request
from flask_login import login_user, redirect

# setup Blueprint
public = Blueprint('public', __name__)


@public.route('/')
def landing():
	"""Landing page"""
	return render_template('public/index.html')


@public.route('/login', methods=['POST', 'GET'])
def login():
	"""Login page"""
	form = LoginForm(request.form)
	user = User(email=form.email.data)
	if request.method == 'POST' and form.validate():
		user.get()
		if user.exists() and user.is_active() \
				and bcrypt.check_password_hash(user.password, form.password.data):

			if login_user(user):
				return redirect(request.args.get('next') or url_for('admin.home'))
		message = 'Login failed.'
	return render_template('public/login.html', **locals())


@public.route('/register')
def register():
	"""Register page"""
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User(
			name=form.name.data,
			email=form.email.data,
			password=bcrypt.generate_password_hash(form.password.data)
		).save()
		if login_user(user):
			return redirect(url_for('sphere.home'))
		else:
			return redirect(url_for('public.login'))
	return render_template('public/register.html', **locals())