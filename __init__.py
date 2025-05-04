from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Configure login manager
login_manager.login_view = 'auth.login' # The blueprint name and function name for the login route
login_manager.login_message_category = 'info' # Optional: category for flash messages

# User loader function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Import the User model here to avoid circular imports
    from .user import User
    return User.query.get(int(user_id))

