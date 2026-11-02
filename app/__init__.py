from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config
import os
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
crsf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    config_mode = os.getenv('CONFIGURATION_MODE', 'development')
    app.config.from_object(config[config_mode])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    crsf.init_app(app)

    from app.routes.auth import auth_bp
    from app.helpers.model import Task, User

    from app.routes.tasks import tasks_bp

    login_manager.login_view = "auth.signin"
    login_manager.login_message = "PLEASE LOGIN FIRST"
    login_manager.login_message_category = "error"

    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    

    with app.app_context():


        


        db.create_all()


    return app
    

@login_manager.user_loader
def load_user(user_id):
    from app.helpers.model import User
    return User.query.get(int(user_id))



    
   