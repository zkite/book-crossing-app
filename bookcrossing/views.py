from bookcrossing import db, api, app, login_manager
from .models import User, Book
from flask import session, url_for, redirect, render_template, request, flash, g, make_response
#from flask_login import login_user, logout_user, current_user, login_required
from flask.ext.login import login_user, logout_user, current_user, login_required
import uuid, json
from .forms import SignUpForm, LoginForm, AddBook
from .utils import AlchemyEncoder
from flask_restful import Resource


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	g.user = current_user


class Index(Resource):
	def get(self):
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('index.html'), 200, headers)

api.add_resource(Index, '/')


class Register(Resource):
	form = None
	headers = {'Content-Type': 'text/html'}

	def get(self):
		self.form = SignUpForm(request.form)
		if session.get('username'):
			flash('You are already logged in')
		return make_response(render_template('register.html', form=self.form), 200, self.headers)

	def post(self):
		username = request.form.get('username')
		password = request.form.get('password')

		existing_user = User.query.filter_by(username=username).first()

		if existing_user:
			flash('This username has been already taken. Try another one', 'alert alert-danger')
			return render_template('register.html', form=self.form)

		user = User(username, password)
		db.session.add(user)
		db.session.commit()
		flash('User successfully registered')
		return redirect(url_for('login'))

api.add_resource(Register, '/register')


class Login(Resource):
	form = None
	headers = {'Content-Type': 'text/html'}

	def get(self):
		self.form = LoginForm(request.form)
		if session.get('username'):
			flash('You are already logged in')

		return make_response(render_template('login.html', form=self.form), 200, self.headers)

	def post(self):
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username, password=password).first()
		if user:
			session['username'] = username
			login_user(user)
			flash('Logged in successfully')
			return redirect(request.args.get('next') or url_for('index'))
		else:
			flash('You are not registered yet')

api.add_resource(Login, '/login')


class Logout(Resource):
	def get(self):
		session.clear()
		logout_user()
		return redirect(url_for('index'))

api.add_resource(Logout, '/logout')



class Books(Resource):
	alchemy_encoder = AlchemyEncoder()
	form = None
	headers = {'Content-Type': 'text/html'}
	shelf = None

	@login_required
	def get(self):
		self.form = AddBook(request.form)
		self.do_shelf()
		return make_response(render_template('books.html', form=self.form, shelf=self.shelf), 200, self.headers)

	@login_required
	def post(self):
		self.form = AddBook(request.form)
		if self.form.validate():
			title = request.form['title']
			author = request.form['author']
			publisher = request.form['publisher']
			category = request.form['category']
			print(title, author, publisher, category)
			book = Book(title, author, publisher, category)

			current_user.books.append(book)
			db.session.add(current_user)
			db.session.commit()

			self.do_shelf()
			return make_response(render_template('books.html', form=self.form, shelf=self.shelf), 200, self.headers)

	def do_shelf(self):
		self.shelf = list()
		for b in current_user.books:
			self.shelf.append(self.alchemy_encoder.default(b))
		self.shelf.reverse()

api.add_resource(Books, '/books')


class Search(Resource):
	books = list()
	alchemy_encoder = AlchemyEncoder()
	headers = {'Content-Type': 'text/html'}

	@login_required
	def post(self):
		query = request.form['search']
		result = Book.query.filter(Book.title.ilike('%'+query+'%'))

		if result:
			for r in result:
				self.books.append(self.alchemy_encoder.default(r))

			return make_response(render_template('search.html', result=self.books), 200, self.headers)
		else:
			return make_response(render_template('search.html'), 200, self.headers)

api.add_resource(Search, '/search')
