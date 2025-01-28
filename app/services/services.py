from flask import Blueprint

services_bp = Blueprint('services', __name__)

@services_bp.route('/')
def services_home():
    return "Services Dashboard"