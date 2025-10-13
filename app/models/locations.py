from ..extensions import db
from .company import Company  # Import Company model to define the relationship

class Location(db.Model):
    __tablename__ = 'locations'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8
    company_id = db.Column(db.BigInteger, db.ForeignKey('company.id'), nullable=False)  # company_id, foreign key to Company table
    name = db.Column(db.String(30), nullable=False)  # name, varchar(30)
    full_name = db.Column(db.String(255), nullable=False)  # full_name, varchar(255)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)

    # Relationship to Company
    company = db.relationship('Company', backref='locations', lazy=True)

    def __repr__(self):
        return f"<Location {self.name}>"
