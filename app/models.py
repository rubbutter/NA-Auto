from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='customer')
    phone = db.Column(db.String(15))
    address = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)
    technician = db.relationship('Technician', backref='profile', uselist=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    vin = db.Column(db.String(17), unique=True)
    mileage = db.Column(db.Integer)
    license_plate = db.Column(db.String(20))

class Technician(db.Model):
    __tablename__ = 'technicians'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    hourly_rate = db.Column(db.Numeric(10, 2))
    is_available = db.Column(db.Boolean, default=True)
    certifications = db.relationship('Certification', backref='technician', lazy=True)
    location = db.Column(db.String(100))  # For geo-fencing
    rating = db.Column(db.Numeric(3, 2), default=0.0)

class Certification(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)  # e.g., ASE_A1 Engine Repair
    date_achieved = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    verification_status = db.Column(db.String(20), default='pending')  # pending/approved/expired
    certificate_number = db.Column(db.String(50))
    verifying_org = db.Column(db.String(100))

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)  # oil_change, brake_service, etc.
    preferred_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending/assigned/in_progress/completed
    assigned_tech = db.Column(db.Integer, db.ForeignKey('technicians.id'))
    notes = db.Column(db.Text)
    price_estimate = db.Column(db.Numeric(10, 2))