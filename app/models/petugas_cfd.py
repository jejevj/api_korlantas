from ..extensions import db
from ..models.company import Company  # Assuming there's a Company model for foreign key reference

class PetugasCfd(db.Model):
    __tablename__ = 'petugas_cfd'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8 (primary key)
    company_id = db.Column(db.BigInteger, db.ForeignKey('company.id'), nullable=False)  # company_id, foreign key to company table
    nama = db.Column(db.String(20), nullable=False)  # nama, varchar(20)
    email = db.Column(db.String(50), nullable=False)  # email, varchar(50)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)
    
    # Relationship to Company (assuming Company table exists)
    company = db.relationship('Company', backref='petugas_cfd', lazy=True)  # Relationship to Company model
    
    def __repr__(self):
        return f"<PetugasCfd {self.nama}>"
