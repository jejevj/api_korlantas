from ..extensions import db
from .company import Company  # Import the Company model
from .locations import Location  # Import the Location model
from .role import Role  # Import the Role model

SENSITIVE_FIELDS = {"password", "mock_password", "reset_password_id"}

class User(db.Model):
    __tablename__ = "users"  # EXACT table name in DB

    id = db.Column(db.BigInteger, primary_key=True)
    company_id = db.Column(db.BigInteger, db.ForeignKey('company.id'), nullable=False)  # Foreign key to Company
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.id'), nullable=True)  # Foreign key to Role
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)
    mock_password = db.Column(db.String(255), nullable=True)
    reset_password_id = db.Column(db.BigInteger, nullable=True)
    full_name = db.Column(db.String(100), nullable=False)
    location_id = db.Column(db.BigInteger, db.ForeignKey('locations.id'), nullable=False)  # Foreign key to Location

    # Relationships
    company = db.relationship('Company', backref='users', lazy=True)  # Relationship to Company model
    role = db.relationship('Role', backref='users', lazy=True)  # Relationship to Role model
    location = db.relationship('Location', backref='users', lazy=True)  # Relationship to Location model

    def to_dict(self, include_sensitive: bool = False):
        cols = self.__table__.columns.keys()
        data = {c: getattr(self, c) for c in cols}
        if not include_sensitive:
            for f in SENSITIVE_FIELDS:
                data.pop(f, None)
        return data

    def __repr__(self):
        return f"<User {self.username}>"
