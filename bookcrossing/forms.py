from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, EqualTo, InputRequired, ValidationError
from flask import current_app
import re


def password_validator(form, field):
	""" Password must have from 6 to 20 characters. """
	password = field.data
	prog = re.compile(r'^[a-z0-9]{6,20}$')
	if not prog.match(password):
		raise ValidationError('Password must have at least 6 characters')


def username_validator(form, field):
	""" Username must have from 6 to 12 characters"""
	username = field.data
	prog = re.compile(r'^[a-z0-9_]{6,12}$')
	if not prog.match(username):
		raise ValidationError("Username may only contain letters, numbers, '-', and have from 6 to 12 characters")


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


class AddBook(Form):
	title = StringField('Title', [InputRequired('Title is required'),
	                              Length(min=6, max=30, message='Title must have from 6 to 30 characters')])
	author = StringField('Author', [InputRequired('Author is required'),
	                              Length(min=6, max=30, message='Author must have from 6 to 30 characters')])
	publisher = StringField('Publisher', [InputRequired('Publisher is required'),
	                              Length(min=6, max=30, message='Publisher must have from 6 to 30 characters')])
	category = StringField('Category', [InputRequired('Category is required'),
	                              Length(min=5, max=30, message='Category must have from 6 to 30 characters')])