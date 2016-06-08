from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, EqualTo, InputRequired


class SignUpForm(Form):
	username = StringField('Username', [InputRequired('Username is required'),
	                                    Length(min=3, max=12, message='Username must have from 3 to 12 characters')])
	password = PasswordField('Password', [InputRequired('Password is required'),
	                                      Length(min=3, max=12, message='Password must have from 3 to 12 characters'),
	                                      EqualTo('confirm', 'Passwords must mutch')])
	confirm = PasswordField('Repeat Password')


class LoginForm(Form):
	username = StringField('Username', [InputRequired('Username is required'),
	                                    Length(min=3, max=12, message='Username must have from 3 to 12 characters')])
	password = PasswordField('Password', [InputRequired('Password is required'),
	                                      Length(min=3, max=12, message='Password must have from 3 to 12 characters')])


class AddBookForm(Form):
	title = StringField('Title', [InputRequired('Title is required'),
	                              Length(min=6, max=30, message='Title must have from 6 to 30 characters')])
	author = StringField('Author', [InputRequired('Author is required'),
	                              Length(min=6, max=30, message='Author must have from 6 to 30 characters')])
	publisher = StringField('Publisher', [InputRequired('Publisher is required'),
	                              Length(min=6, max=30, message='Publisher must have from 6 to 30 characters')])
	category = StringField('Category', [InputRequired('Category is required'),
	                              Length(min=6, max=30, message='Category must have from 6 to 30 characters')])


class SearchForm(Form):
	search = StringField('Search', [InputRequired(), Length(min=3, max=30)])