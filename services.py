from flask import Blueprint, request, jsonify
from app.models import Service
from main import db

services_blueprint = Blueprint('services', __name__)

@services_blueprint.route('/', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{"id": s.id, "name": s.name, "price": s.price} for s in services]), 200

@services_blueprint.route('/', methods=['POST'])
def add_service():
    data = request.get_json()
    service = Service(name=data['name'], price=data['price'], description=data.get('description'))
    db.session.add(service)
    db.session.commit()
    return jsonify({"message": "Service added successfully"}), 201
