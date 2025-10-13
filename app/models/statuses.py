from ..extensions import db

class Status(db.Model):
    __tablename__ = 'statuses'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8
    name = db.Column(db.String(10), nullable=False)  # name, varchar(10)
    caption = db.Column(db.String(50), nullable=False)  # caption, varchar(50)
    description = db.Column(db.String(255), nullable=False)  # description, varchar(255)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(255), nullable=False, default='pg_catalog')  # changed_by, varchar(255)

    def __repr__(self):
        return f"<Status {self.name}>"
