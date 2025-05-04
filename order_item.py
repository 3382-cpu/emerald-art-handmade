from . import db
from .product import Product
from .order import Order

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False) # Price per item at the time of purchase
    selected_color = db.Column(db.String(50), nullable=True) # Store the selected color

    # Relationships
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))
    # order is defined in Order model via backref

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Product:{self.product_id} Qty:{self.quantity}>'

