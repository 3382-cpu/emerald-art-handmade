from . import db
import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    description_ar = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False) # Store price in USD
    image_urls = db.Column(db.JSON, nullable=True) # Store list of image URLs
    available_colors = db.Column(db.JSON, nullable=True) # Store list of available colors (e.g., ['pink', 'red', 'white'])
    category = db.Column(db.String(50), nullable=False) # e.g., 'bouquet', 'mirror'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    # reviews = db.relationship('Review', backref='product', lazy=True)
    # order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name_en}>'

