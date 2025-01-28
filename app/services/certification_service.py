from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Certification, Technician, User, db
from datetime import datetime, timedelta

cert_bp = Blueprint('certifications', __name__)

# ASE Test Types (Partial list - expand based on https://www.ase.com/ase-certification-tests)
ASE_TESTS = {
    'A1': 'Engine Repair',
    'A2': 'Automatic Transmission/Transaxle',
    'A3': 'Manual Drive Train & Axles',
    'A4': 'Suspension & Steering',
    'A5': 'Brakes',
    'A6': 'Electrical/Electronic Systems',
    'A7': 'Heating & Air Conditioning',
    'A8': 'Engine Performance'
}

@cert_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_certification():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.technician:
        return jsonify(message="Only technicians can apply for certifications"), 403
        
    data = request.json
    test_code = data.get('test_code')
    
    if test_code not in ASE_TESTS:
        return jsonify(message="Invalid ASE test code"), 400
    
    # Calculate expiry (ASE certs typically valid for 5 years)
    expiry_date = datetime.now() + timedelta(days=5*365)
    
    new_cert = Certification(
        tech_id=user.technician.id,
        test_type=f"ASE_{test_code}",
        date_achieved=datetime.now(),
        expiry_date=expiry_date,
        verification_status='pending',
        verifying_org='Automotive Service Excellence (ASE)'
    )
    
    db.session.add(new_cert)
    db.session.commit()
    
    return jsonify(message="Certification application submitted", 
                 certification=new_cert.to_dict()), 201

@cert_bp.route('/verify/<int:cert_id>', methods=['POST'])
@jwt_required()
def verify_certification(cert_id):
    # Admin-only endpoint
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'admin':
        return jsonify(message="Admin access required"), 403
    
    cert = Certification.query.get(cert_id)
    if not cert:
        return jsonify(message="Certification not found"), 404
    
    data = request.json
    cert.verification_status = data.get('status', 'approved')
    cert.certificate_number = data.get('certificate_number')
    
    db.session.commit()
    return jsonify(message="Certification updated", certification=cert.to_dict())

# Add model to_dict() methods for JSON serialization
def model_to_dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}

Certification.to_dict = lambda self: model_to_dict(self)
Technician.to_dict = lambda self: model_to_dict(self)

@cert_bp.route('/dashboard', methods=['GET'])
@jwt_required
def tech_dashboard():
    user_id = get_jwt_identity()
    tech = Technician.query.filter_by(user_id=user_id).first()
    
    if not tech or tech.verification_status != 'approved':
        return redirect(url_for('auth.profile'))
    
    requests = ServiceRequest.query.filter_by(
        assigned_tech=tech.id,
        status='assigned'
    ).all()
    
    return render_template('tech_dashboard.html',
                         requests=requests,
                         tech=tech)