from ..extensions import db

class MasterDyn(db.Model):
    __tablename__ = 'master_dyn'

    # Columns mapping based on the provided schema
    master_id = db.Column(db.BigInteger, primary_key=True)  # master_id, type int8 (primary key)
    status_id = db.Column(db.BigInteger, nullable=False)  # status_id, type int8
    inspected_id = db.Column(db.BigInteger, nullable=False)  # inspected_id, type int8
    inspected_at = db.Column(db.TIMESTAMP, nullable=False)  # inspected_at, timestamp
    verified_id = db.Column(db.BigInteger, nullable=False)  # verified_id, type int8
    verified_at = db.Column(db.TIMESTAMP, nullable=False)  # verified_at, timestamp
    sent_at = db.Column(db.TIMESTAMP, nullable=False)  # sent_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, nullable=False)  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)

    def __repr__(self):
        return f"<MasterDyn {self.master_id}>"
