from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config  # Import configuration
from models.models import User
from models.models import db 
from flask_mail import Mail

# Initialize the extensions

bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

# App Factory
def create_app():
    # Create the app instance
    app = Flask(__name__, template_folder="templates")
   
    # Load Configuration from config.py
    app.config.from_object(Config)
    

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)  # Migrate is initialized with db
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'auth.login'

  # Define the user_loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Assuming user_id is an integer
    
    # Import and register blueprints
    from blueprints.auth.routes import auth
    from blueprints.admin.routes import admin
    from blueprints.quiz.routes import quiz
    from blueprints.user.routes import user
    from blueprints.main.routes import main

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(quiz, url_prefix='/quiz')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(main)  # Register the main blueprint

    return app
