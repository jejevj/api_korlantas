from ..extensions import db

class MasterStatusHist(db.Model):
    __tablename__ = 'master_status_hist'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8 (primary key)
    master_id = db.Column(db.BigInteger, nullable=False)  # master_id, int8 (foreign key)
    status_id = db.Column(db.BigInteger, nullable=False)  # status_id, int8 (foreign key)
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)
    changed_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # changed_at, timestamp

    def __repr__(self):
        return f"<MasterStatusHist {self.id} - Master {self.master_id}>"
