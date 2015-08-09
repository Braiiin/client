from flask import Blueprint, render_template
from flask_login import login_required

# setup Blueprint
sphere = Blueprint('sphere', __name__)


@sphere.route('/home')
@login_required
def home():
	"""Landing page"""
	return render_template('sphere/home.html')