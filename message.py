from . import db
from .user import User
from .order import Order # Optional: Link message to an order
import datetime

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Null if message is to admin group
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True) # Optional link to order
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy=True))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_messages', lazy=True))
    order = db.relationship('Order', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message {self.id} From:{self.sender_id} To:{self.receiver_id}>'

