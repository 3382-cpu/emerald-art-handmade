from flask import Blueprint, request, jsonify
from src.models import db
from src.models.message import Message
from src.models.user import User
from flask_login import login_required, current_user

messages_bp = Blueprint("messages", __name__)

@messages_bp.route("/send", methods=["POST"])
@login_required
def send_message():
    data = request.get_json()
    receiver_email = data.get("receiver_email") # Send to specific user or admin
    subject = data.get("subject")
    body = data.get("body")
    order_id = data.get("order_id") # Optional: link to an order

    if not subject or not body:
        return jsonify({"error": "Subject and body are required"}), 400

    receiver = None
    if receiver_email:
        receiver = User.query.filter_by(email=receiver_email).first()
        if not receiver:
            return jsonify({"error": "Receiver not found"}), 404
        receiver_id = receiver.id
    else:
        # Default to sending to admin (or handle differently)
        # For simplicity, let's assume sending to a generic admin or requires specific receiver
        # This needs refinement based on how admin communication is handled
        # Maybe find first admin user?
        admin_user = User.query.filter_by(role="admin").first()
        if not admin_user:
             return jsonify({"error": "Admin user not found to receive message"}), 404
        receiver_id = admin_user.id # Send to the first admin found

    try:
        new_message = Message(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            subject=subject,
            body=body,
            order_id=order_id # Can be None
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify({"message": "Message sent successfully", "message_id": new_message.id}), 201
    except Exception as e:
        db.session.rollback()
        # Log the error e
        return jsonify({"error": "Failed to send message"}), 500

@messages_bp.route("/inbox", methods=["GET"])
@login_required
def get_inbox():
    # Get messages received by the current user
    try:
        messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()
        message_list = [
            {
                "id": msg.id,
                "subject": msg.subject,
                "sender_email": msg.sender.email,
                "is_read": msg.is_read,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
        return jsonify(message_list), 200
    except Exception as e:
        # Log the error e
        return jsonify({"error": "Failed to retrieve inbox"}), 500

@messages_bp.route("/sent", methods=["GET"])
@login_required
def get_sent_messages():
    # Get messages sent by the current user
    try:
        messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
        message_list = [
            {
                "id": msg.id,
                "subject": msg.subject,
                "receiver_email": msg.receiver.email if msg.receiver else "Admin", # Handle admin case
                "is_read": msg.is_read,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
        return jsonify(message_list), 200
    except Exception as e:
        # Log the error e
        return jsonify({"error": "Failed to retrieve sent messages"}), 500

@messages_bp.route("/<int:message_id>", methods=["GET"])
@login_required
def get_message_detail(message_id):
    try:
        message = Message.query.get_or_404(message_id)
        # Check if the current user is the sender or receiver
        if message.sender_id != current_user.id and message.receiver_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403

        # Mark as read if the current user is the receiver
        if message.receiver_id == current_user.id and not message.is_read:
            message.is_read = True
            db.session.commit()

        return jsonify({
            "id": message.id,
            "subject": message.subject,
            "body": message.body,
            "sender_email": message.sender.email,
            "receiver_email": message.receiver.email if message.receiver else "Admin",
            "order_id": message.order_id,
            "is_read": message.is_read,
            "created_at": message.created_at.isoformat()
        }), 200
    except Exception as e:
        db.session.rollback()
        # Log the error e
        return jsonify({"error": "Failed to retrieve message details"}), 500

# Add route for marking messages as read/unread or deleting messages if needed

