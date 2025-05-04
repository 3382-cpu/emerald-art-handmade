from . import db
from .user import User
import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending') # e.g., Pending, Processing, Shipped, Delivered, Cancelled
    total_price = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    customer = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    # messages = db.relationship('Message', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'

