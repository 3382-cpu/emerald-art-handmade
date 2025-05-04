from flask import Blueprint, request, jsonify
from src.models import db, bcrypt
from src.models.user import User
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409

    # Create new user (consider adding more fields like name, etc.)
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Log in the user automatically after registration
    login_user(new_user)

    return jsonify({"message": "User registered successfully", "user": {"id": new_user.id, "email": new_user.email, "role": new_user.role}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user) # Manages session
        return jsonify({"message": "Login successful", "user": {"id": user.id, "email": user.email, "role": user.role}}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@auth_bp.route("/logout", methods=["POST"])
@login_required # Ensure user is logged in to log out
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route("/status")
@login_required
def status():
    # Route to check current login status and user info
    return jsonify({"logged_in": True, "user": {"id": current_user.id, "email": current_user.email, "role": current_user.role}}), 200

# Add more auth routes if needed (e.g., password reset)

