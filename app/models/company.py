from ..extensions import db

class Company(db.Model):
    __tablename__ = 'company'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8 (primary key)
    company_name = db.Column(db.String(100), nullable=False)  # company_name, varchar(100)
    company_logo = db.Column(db.String(255), nullable=False)  # company_logo, varchar(255)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)

    def __repr__(self):
        return f"<Company {self.company_name}>"
