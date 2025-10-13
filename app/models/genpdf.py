from ..extensions import db

class Genpdf(db.Model):
    __tablename__ = 'genpdf'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8 (primary key)
    master_id = db.Column(db.BigInteger, nullable=False)  # master_id, foreign key from master table
    valid_content = db.Column(db.Boolean, nullable=False, default=False)  # valid_content, bool
    pdf_format1 = db.Column(db.String(255), nullable=False)  # pdf_format1, varchar(255)
    pdf_format2 = db.Column(db.String(255), nullable=False)  # pdf_format2, varchar(255)
    pdf_format3 = db.Column(db.String(255), nullable=False)  # pdf_format3, varchar(255)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)


    def __repr__(self): 
        return f"<Genpdf {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "master_id": self.master_id,
            "valid_content": self.valid_content,
            "pdf_format1": self.pdf_format1,
            "pdf_format2": self.pdf_format2,
            "pdf_format3": self.pdf_format3,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "changed_by": self.changed_by
        }
