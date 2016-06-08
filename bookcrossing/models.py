from bookcrossing import db

userBooks = db.Table('userBooks', db.Model.metadata,
	db.Column('user_id', db.ForeignKey('users.id'), nullable=False),
	db.Column('book_id', db.ForeignKey('books.id'), nullable=False)
)


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, primary_key=True)
	username = db.Column('username', db.String(20), unique=True, index=True, nullable=False)
	password = db.Column('password', db.String(30), nullable=False)

	books = db.relationship('Book', secondary=userBooks, backref='users')

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def __eq__(self, user):
		return self.name == user.name


class Book(db.Model):
	__tablename__ = 'books'

	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.String, nullable=False)
	author = db.Column('author', db.String, nullable=False)
	publisher = db.Column('publisher', db.String, nullable=False)
	category = db.Column('category', db.String, nullable=False)


	def __init__(self, title, author, publisher, category):
		self.title = title
		self.author = author
		self.publisher = publisher
		self.category = category