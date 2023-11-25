from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

class Asset(db.Model, SerializerMixin):
    __tablename__ = 'asset'

    serialize_rules = ('-assignments.asset', '-maintenances.asset', '-transactions.asset')

    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))
    date_purchased = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))
    category = db.Column(db.String(50))
    
    # Relationships
    assignments = db.relationship('Assignment', back_populates='asset')
    maintenances = db.relationship('Maintenance', back_populates='asset')
    transactions = db.relationship('Transaction', back_populates='asset')

    @validates('status')
    def validate_status(self, _, value):
        if value not in ['Active', 'Pending', 'Under Maintenance']:
            raise ValueError(f"Invalid status: {value}. Must be 'Active', 'Pending', or 'Under Maintenance'.")
        return value

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'

    serialize_rules = ('-assignments.user', '-requests.user')
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    _password_hash = db.Column('password_hash', db.String(255), nullable=False)
    role = db.Column(db.String(50))
    department = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    assignments = db.relationship('Assignment', back_populates='user')
    requests = db.relationship('Requests', back_populates='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('password hash may not be viewed')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('email')
    def validate_email(self, key, value):
        if not value or '@' not in value:
            raise ValueError("Invalid email address.")
        return value

class Assignment(db.Model, SerializerMixin):
    __tablename__ = 'assignment'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assignment_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    # Relationships
    asset = db.relationship('Asset', back_populates='assignments')
    user = db.relationship('User', back_populates='assignments')

class Maintenance(db.Model, SerializerMixin):
    __tablename__ = 'maintenance'
    serialize_rules = ('-asset.maintenances',)
    
    maintenance_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    date_of_maintenance = db.Column(db.Date)
    type = db.Column(db.String(50))
    description = db.Column(db.String(255))

    # Relationships
    asset = db.relationship('Asset', back_populates='maintenances')

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    transaction_date = db.Column(db.Date)
    transaction_type = db.Column(db.String(50))

    # Relationships
    asset = db.relationship('Asset', back_populates='transactions')

class Requests(db.Model, SerializerMixin):
    __tablename__ = 'requests'
    serialize_rules = ('-user.requests',)
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(255))
    status = db.Column(db.String(50))
    asset_name = db.Column(db.String(255))

    # Relationships
    user = db.relationship('User', back_populates='requests')
