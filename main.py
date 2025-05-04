import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Import extensions and models
from src.models import db, migrate, bcrypt, login_manager
# Import all models to ensure they are registered with SQLAlchemy
from src.models.user import User
from src.models.product import Product
from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.review import Review
from src.models.message import Message

# Import blueprints
from src.routes.auth import auth_bp
from src.routes.products import products_bp
from src.routes.orders import orders_bp
from src.routes.reviews import reviews_bp
from src.routes.messages import messages_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=None) # Disable default static folder handling
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-in-production")

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}}) # Adjust origins for production

# Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv("DB_USERNAME", "root")}:{os.getenv("DB_PASSWORD", "password")}@{os.getenv("DB_HOST", "localhost")}:{os.getenv("DB_PORT", "3306")}/{os.getenv("DB_NAME", "emerald_art_db")}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(products_bp, url_prefix="/api/products")
app.register_blueprint(orders_bp, url_prefix="/api/orders")
app.register_blueprint(reviews_bp, url_prefix="/api/reviews")
app.register_blueprint(messages_bp, url_prefix="/api/messages")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

# Simple route for testing API is up
@app.route("/api/health")
def health_check():
    return {"status": "ok"}

# Catch-all route for non-API requests (optional, depends on deployment strategy)
# @app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
# def catch_all(path):
#     # Could redirect to the frontend URL or serve a minimal HTML page
#     return "API Endpoint", 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    # Note: debug=True should be False in production
    app.run(host="0.0.0.0", port=port, debug=True)

