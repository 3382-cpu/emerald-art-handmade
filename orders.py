from flask import Blueprint, request, jsonify
from src.models import db
from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.product import Product
from src.models.user import User
from flask_login import login_required, current_user

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/", methods=["POST"])
@login_required
def create_order():
    data = request.get_json()
    items = data.get("items") # Expected format: [{ "product_id": 1, "quantity": 2, "selected_color": "pink" }, ...]
    shipping_address = data.get("shipping_address")
    country = data.get("country")

    if not items or not shipping_address or not country:
        return jsonify({"error": "Missing required order information"}), 400

    total_price = 0
    order_items_to_create = []

    try:
        for item_data in items:
            product = Product.query.get(item_data.get("product_id"))
            if not product:
                return jsonify({"error": f"Product with id {item_data.get('product_id')} not found"}), 404
            
            quantity = item_data.get("quantity", 1)
            price_at_purchase = product.price # Use current product price
            total_price += price_at_purchase * quantity
            
            order_item = OrderItem(
                product_id=product.id,
                quantity=quantity,
                price_at_purchase=price_at_purchase,
                selected_color=item_data.get("selected_color")
            )
            order_items_to_create.append(order_item)

        # Create the order
        new_order = Order(
            user_id=current_user.id,
            total_price=total_price,
            shipping_address=shipping_address,
            country=country,
            status="Pending" # Initial status
        )
        
        # Add items to the order
        new_order.items.extend(order_items_to_create)
        
        db.session.add(new_order)
        db.session.commit()

        # Here you would typically trigger payment processing or display payment instructions
        # For now, just return the created order details
        return jsonify({
            "message": "Order created successfully. Please proceed with payment.",
            "order_id": new_order.id,
            "status": new_order.status,
            "total_price": new_order.total_price,
            # Add payment details/instructions here based on chosen method (Bank/PayPal)
            "payment_instructions": "Please transfer the total amount to Bank Account: XXXX-XXXX-XXXX or PayPal: user@example.com. Use your Order ID as reference."
        }), 201

    except Exception as e:
        db.session.rollback()
        # Log the error e
        return jsonify({"error": "Failed to create order"}), 500

@orders_bp.route("/", methods=["GET"])
@login_required
def get_user_orders():
    # Get orders for the currently logged-in user
    try:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        order_list = []
        for order in orders:
            items = [{ "product_id": item.product_id, "name": item.product.name_en, "quantity": item.quantity, "price": item.price_at_purchase, "color": item.selected_color } for item in order.items]
            order_list.append({
                "id": order.id,
                "status": order.status,
                "total_price": order.total_price,
                "created_at": order.created_at.isoformat(),
                "items": items
            })
        return jsonify(order_list), 200
    except Exception as e:
        # Log the error e
        return jsonify({"error": "Failed to retrieve orders"}), 500

# Add routes for getting specific order details, updating status (admin), etc.

