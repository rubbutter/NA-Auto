from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from auth import auth_bp
#from services import services_blueprint

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Adjust your DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    return "Welcome to the Automotive Service App!"

# Register blueprints
#app.register_blueprint(auth_bp, url_prefix='/auth')
#app.register_blueprint(services_blueprint, url_prefix='/services')

if __name__ == "__main__":
    app.run(debug=True)
