from ..extensions import db

class StoragePath(db.Model):
    __tablename__ = 'storages_path'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8
    name = db.Column(db.String(20), nullable=False)  # name, varchar(20)
    path = db.Column(db.String(2024), nullable=False)  # path, varchar(2024)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(255), nullable=False, default='pg_catalog')  # changed_by, varchar(255)

    def __repr__(self):
        return f"<StoragePath {self.name}>"
