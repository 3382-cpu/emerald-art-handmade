from flask import Blueprint, request, jsonify
from src.models import db
from src.models.product import Product

products_bp = Blueprint("products", __name__)

@products_bp.route("/", methods=["GET"])
def get_products():
    # Add filtering/pagination later if needed
    try:
        products = Product.query.all()
        product_list = [
            {
                "id": p.id,
                "name_en": p.name_en,
                "name_ar": p.name_ar,
                "description_en": p.description_en,
                "description_ar": p.description_ar,
                "price": p.price,
                "image_urls": p.image_urls,
                "available_colors": p.available_colors,
                "category": p.category,
            }
            for p in products
        ]
        return jsonify(product_list), 200
    except Exception as e:
        # Log the error e
        return jsonify({"error": "Failed to retrieve products"}), 500

@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            "id": product.id,
            "name_en": product.name_en,
            "name_ar": product.name_ar,
            "description_en": product.description_en,
            "description_ar": product.description_ar,
            "price": product.price,
            "image_urls": product.image_urls,
            "available_colors": product.available_colors,
            "category": product.category,
            # Add reviews relationship later if needed
        }), 200
    except Exception as e:
        # Log the error e
        return jsonify({"error": "Product not found or failed to retrieve"}), 404

# Admin routes for creating/updating/deleting products will be added later in admin.py

