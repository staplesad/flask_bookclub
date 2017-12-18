from bookclub_app import db
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import generate_password_hash, check_password_hash

##PASSWORD FUNCTIONS##
def hash_password( password):
    return generate_password_hash(password)

def check_password( hashed_password, given_password):
    return check_password_hash(hashed_password, given_password)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(72), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(120), index=False, unique=False)

    books = db.relationship('Book', backref='author', lazy='dynamic')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    wishbook = db.relationship('WishBook', backref='user', lazy='dynamic')
    poll = db.relationship('Poll', backref='user', lazy='dynamic')
    pollresult = db.relationship('PollResult', backref='user', lazy='dynamic')

    def __init__(self, name, email, password):
        self.nickname = name
        self.email = email
        self.hashed_password = hash_password(password)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) #python 2
        except NameError:
            return str(self.id) #python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, unique=True)
    due_date = db.Column(db.Date)
    info = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviews = db.relationship('Review', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Book %r>' % self.title

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer)
    text = db.Column(db.String(550))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Review %r>' % self.star

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_text = db.Column(db.String(550))

    def __repr__(self):
        return '<Quote %r>' % self.quote_text

class WishBook(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    author = db.Column(db.String(255))
    info = db.Column(db.String(550))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Book %r>' % self.title
class Poll(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date)
    closed=db.Column(db.Boolean, default=False)
    info=db.Column(db.String(2000))
    options=db.Column(ARRAY(db.String))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    
    pollresult = db.relationship('PollResult', backref='poll', lazy='dynamic')

    def __repr__(self):
        return '<Poll by %r at %r: %r>' % self.user_id, self.date, self.options

class PollResult(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_choice=db.Column(db.String(255))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    poll_id=db.Column(db.Integer, db.ForeignKey('poll.id'))
