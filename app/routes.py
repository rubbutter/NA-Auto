from flask import render_template, request, redirect, url_for
from flask_jwt_extended import jwt_optional, get_jwt_identity
from app import app
from app.models import User, ServiceRequest, Vehicle

@app.route('/')
@jwt_optional
def home():
    return render_template('home.html')

@app.route('/services')
@jwt_required
def services():
    user_id = get_jwt_identity()
    vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    return render_template('services.html', vehicles=vehicles)

@app.route('/book', methods=['POST'])
@jwt_required
def book_service():
    data = request.form
    new_request = ServiceRequest(
        user_id=get_jwt_identity(),
        vehicle_id=data['vehicle'],
        service_type=data['service_type'],
        preferred_time=data['datetime'],
        notes=data.get('notes', '')
    )
    db.session.add(new_request)
    db.session.commit()
    
    # TODO: Implement technician matching
    return redirect(url_for('booking_status', request_id=new_request.id))