from flask import Blueprint, request, jsonify
from src.models import db
from src.models.product import Product
from src.models.order import Order
from src.models.user import User
from flask_login import login_required
from src.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)

# --- Product Management ---

@admin_bp.route("/products", methods=["POST"])
@admin_required
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            name_en=data.get("name_en"),
            name_ar=data.get("name_ar"),
            description_en=data.get("description_en"),
            description_ar=data.get("description_ar"),
            price=float(data.get("price")),
            image_urls=data.get("image_urls", []),
            available_colors=data.get("available_colors", []),
            category=data.get("category", "bouquet")
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully", "product_id": new_product.id}), 201
    except Exception as e:
        db.session.rollback()
        # Log error e
        return jsonify({"error": f"Failed to create product: {str(e)}"}), 500

@admin_bp.route("/products/<int:product_id>", methods=["PUT"])
@admin_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    try:
        product.name_en = data.get("name_en", product.name_en)
        product.name_ar = data.get("name_ar", product.name_ar)
        product.description_en = data.get("description_en", product.description_en)
        product.description_ar = data.get("description_ar", product.description_ar)
        product.price = float(data.get("price", product.price))
        product.image_urls = data.get("image_urls", product.image_urls)
        product.available_colors = data.get("available_colors", product.available_colors)
        product.category = data.get("category", product.category)
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        # Log error e
        return jsonify({"error": f"Failed to update product: {str(e)}"}), 500

@admin_bp.route("/products/<int:product_id>", methods=["DELETE"])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        # Log error e
        return jsonify({"error": f"Failed to delete product: {str(e)}"}), 500

# --- Order Management ---

@admin_bp.route("/orders", methods=["GET"])
@admin_required
def get_all_orders():
    # Add filtering/pagination later
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        order_list = []
        for order in orders:
            items = [{ "product_id": item.product_id, "name": item.product.name_en, "quantity": item.quantity, "price": item.price_at_purchase, "color": item.selected_color } for item in order.items]
            order_list.append({
                "id": order.id,
                "user_email": order.customer.email,
                "status": order.status,
                "total_price": order.total_price,
                "shipping_address": order.shipping_address,
                "country": order.country,
                "created_at": order.created_at.isoformat(),
                "items": items
            })
        return jsonify(order_list), 200
    except Exception as e:
        # Log error e
        return jsonify({"error": f"Failed to retrieve orders: {str(e)}"}), 500

@admin_bp.route("/orders/<int:order_id>/status", methods=["PUT"])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    new_status = data.get("status")
    
    # Add validation for allowed statuses
    allowed_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    if not new_status or new_status not in allowed_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(allowed_statuses)}"}), 400
        
    try:
        order.status = new_status
        db.session.commit()
        return jsonify({"message": f"Order {order_id} status updated to {new_status}"}), 200
    except Exception as e:
        db.session.rollback()
        # Log error e
        return jsonify({"error": f"Failed to update order status: {str(e)}"}), 500

# --- User Management (Optional - Add if needed) ---
# @admin_bp.route("/users", methods=["GET"])
# @admin_required
# def get_all_users():
#     pass

# @admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
# @admin_required
# def update_user_role(user_id):
#     pass

