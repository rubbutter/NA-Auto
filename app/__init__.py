from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from flask_socketio import SocketIO

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.auth import auth_bp
    from app.services import services_bp
    from app.services.certification_service import cert_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(cert_bp, url_prefix='/certifications')

    with app.app_context():
        db.create_all()

    socketio.init_app(app) 
    return app

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
socketio = SocketIO() 