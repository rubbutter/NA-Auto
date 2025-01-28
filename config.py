import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_na_auto')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:FionaFrancesca1%21@localhost/na_auto')  # Encoded password
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    ASE_API_KEY = os.getenv('ASE_API_KEY')