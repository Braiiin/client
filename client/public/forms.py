from client.forms import Form, wtf


class LoginForm(Form):
	username = wtf.StringField('Username')
	password = wtf.StringField('Password')


class RegisterForm(Form):
	name = wtf.StringField('Full Name')
	username = wtf.StringField('Username')
	email = wtf.StringField('Email')
	password = wtf.StringField('Password')