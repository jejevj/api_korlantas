from ..extensions import db

class Enumeration(db.Model):
    __tablename__ = 'enumerations'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8
    groupname = db.Column(db.String(20), nullable=False)  # groupname, varchar(20)
    name = db.Column(db.String(50), nullable=False)  # name, varchar(50)
    value_type = db.Column(db.String(10), nullable=False)  # value_type, varchar(10)
    value_number = db.Column(db.SmallInteger, nullable=False)  # value_number, int2
    value_string = db.Column(db.String(100), nullable=False)  # value_string, varchar(100)
    value_date = db.Column(db.Date, nullable=False)  # value_date, date
    value_time = db.Column(db.Time, nullable=False)  # value_time, time
    value_timestamp = db.Column(db.TIMESTAMP, nullable=False)  # value_timestamp, timestamp
    description = db.Column(db.String(255), nullable=False)  # description, varchar(255)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(255), nullable=False, default='pg_catalog')  # changed_by, varchar(255)

    def __repr__(self):
        return f"<Enumeration {self.name}>"
