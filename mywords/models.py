from mywords import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=False, index=True)
	password_hash = db.Column(db.String(128))

	# relationship
	words = db.relationship('Words', backref='users',lazy='dynamic')

	def __init__(self, email, first_name, last_name, password):
		self.email = email
		self.username = first_name.strip()+" "+last_name.strip()
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return f"UserName: {self.username} Email: {self.email}"

class Words(db.Model):
	__tablename__ = "words"
	id = db.Column(db.Integer, primary_key = True)
	word = db.Column(db.String(45), unique=False, index=True)
	word_data = db.Column(db.String, unique=False, index=True)
	comment = db.Column(db.String(300), unique=False, index=True)

	# relationship
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

	def __init__(self, user_id, word, word_data, comment):
		self.user_id = user_id
		self.word = word.strip()
		self.word_data = word_data.strip()
		self.comment = comment.strip()

#db.create_all()