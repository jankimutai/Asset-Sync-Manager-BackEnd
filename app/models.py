from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

class Asset(db.Model, SerializerMixin):
    __tablename__ = 'asset'
    serialize_rules = ('-assignments.asset', '-maintenances.asset', '-transactions.asset')
    assetID = db.Column(db.Integer, primary_key=True)
    assetName = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    imageUrl = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))
    datePurchased = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))
    category = db.Column(db.String(50))

    assignments = db.relationship('Assignment', backref='asset')
    maintenances = db.relationship('Maintenance', backref='asset')
    transactions = db.relationship('Transaction', backref='asset')

    @validates('status')
    def validate_status(self, _, value):
        if value not in ['Active', 'Pending', 'Under Maintenance']:
            raise ValueError(f"Invalid status: {value}. Must be 'Active', 'Pending', or 'Under Maintenance'.")
        return value

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    serialize_rules = ('-assignments.user', '-requests.user')
    userid = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    _password_hash = db.Column('password_hash', db.String(255), nullable=False)
    role = db.Column(db.String(50))
    department = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship('Assignment', backref='user')
    requests = db.relationship('Requests', backref='user')

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
    assetID = db.Column(db.Integer, db.ForeignKey('asset.assetID'))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    assignmentDate = db.Column(db.Date)
    returnDate = db.Column(db.Date)

class Maintenance(db.Model, SerializerMixin):
    __tablename__ = 'maintenance'
    serialize_rules = ('-asset.maintenances',)
    maintenanceId = db.Column(db.Integer, primary_key=True)
    assetID = db.Column(db.Integer, db.ForeignKey('asset.assetID'))
    dateofmaintenance = db.Column(db.Date)
    type = db.Column(db.String(50))
    description = db.Column(db.String(255))

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transaction'
    transactionid = db.Column(db.Integer, primary_key=True)
    assetID = db.Column(db.Integer, db.ForeignKey('asset.assetID'))
    transactionDate = db.Column(db.Date)
    transactiontype = db.Column(db.String(50))

class Requests(db.Model, SerializerMixin):
    __tablename__ = 'requests'
    serialize_rules = ('-user.requests',)
    requestID = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    description = db.Column(db.String(255))
    status = db.Column(db.String(50))
    assetName = db.Column(db.String(255))

    user = db.relationship('User', backref='requests')
