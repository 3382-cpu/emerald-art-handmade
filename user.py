from . import db, bcrypt
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer') # 'customer' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships (add later as needed)
    # orders = db.relationship('Order', backref='customer', lazy=True)
    # reviews = db.relationship('Review', backref='author', lazy=True)
    # messages = db.relationship('Message', backref='sender', lazy=True)

    def __init__(self, email, password, role='customer'):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.email}>'

