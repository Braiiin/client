from app.forms import Form, wtf


class LoginForm(Form):
	email = wtf.StringField('Email')
	password = wtf.StringField('Password')


class RegisterForm(Form):
	name = wtf.StringField('Full Name')
	email = wtf.StringField('Email')
	password = wtf.StringField('Password')