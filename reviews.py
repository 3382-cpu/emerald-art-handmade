from flask import Blueprint, request, jsonify
from src.models import db
from src.models.review import Review
from src.models.product import Product
from flask_login import login_required, current_user

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/product/<int:product_id>", methods=["GET"])
def get_product_reviews(product_id):
    # Get reviews for a specific product
    try:
        # Ensure product exists (optional, depends on desired behavior)
        # product = Product.query.get_or_404(product_id)
        
        reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
        review_list = [
            {
                "id": review.id,
                "rating": review.rating,
                "comment": review.comment,
                "user_email": review.author.email, # Or user name if available
                "created_at": review.created_at.isoformat()
            }
            for review in reviews
        ]
        return jsonify(review_list), 200
    except Exception as e:
        # Log the error e
        return jsonify({"error": "Failed to retrieve reviews"}), 500

@reviews_bp.route("/", methods=["POST"])
@login_required
def submit_review():
    data = request.get_json()
    product_id = data.get("product_id")
    rating = data.get("rating")
    comment = data.get("comment")

    if not product_id or not rating:
        return jsonify({"error": "Product ID and rating are required"}), 400

    # Validate rating (e.g., 1-5)
    try:
        rating = int(rating)
        if not 1 <= rating <= 5:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid rating value. Must be an integer between 1 and 5."}), 400

    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Optional: Check if user has already reviewed this product
    existing_review = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_review:
        return jsonify({"error": "You have already reviewed this product"}), 409
        
    # Optional: Check if user purchased the product before allowing review (more complex logic needed)

    try:
        new_review = Review(
            user_id=current_user.id,
            product_id=product_id,
            rating=rating,
            comment=comment
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review submitted successfully", "review_id": new_review.id}), 201
    except Exception as e:
        db.session.rollback()
        # Log the error e
        return jsonify({"error": "Failed to submit review"}), 500

# Add admin routes for managing reviews if needed

