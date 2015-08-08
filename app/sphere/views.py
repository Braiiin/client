from flask import Blueprint, render_template

# setup Blueprint
sphere = Blueprint('sphere', __name__)


@sphere.route('/home')
def home():
	"""Landing page"""
	return render_template('sphere/home.html')