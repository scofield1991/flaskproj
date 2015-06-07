from app import db
from werkzeug import generate_password_hash, check_password_hash

ROLE_USER=0
ROLE_ADMIN=1

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nickname=db.Column(db.String(64), index=True, unique=True)
    password=db.Column(db.String(10))
    email=db.Column(db.String(120), index=True, unique=True)
    role=db.Column(db.SmallInteger, default=ROLE_USER)
    posts=db.relationship('Post', backref='author', lazy='dynamic')
    answers=db.relationship('Answer', backref='author', lazy='dynamic')

    def __init__(self, nickname, email, password):
        self.nickname = nickname
        self.email = email.lower()
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
   
    def check_password(self, passw):
        return check_password_hash(self.password, passw)
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers=db.relationship('Answer', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    likes=db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Answer %r>' % (self.body)
