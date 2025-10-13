from ..extensions import db

class MasterCore(db.Model):
    __tablename__ = 'master_core'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8
    cfd_id = db.Column(db.BigInteger, nullable=False)  # cfd_id, int8 (foreign key from cfd)
    xdata_id = db.Column(db.BigInteger, nullable=False)  # xdata_id, int8 (foreign key from xdata)
    genpdf_id = db.Column(db.BigInteger, nullable=False)  # genpdf_id, int8 (foreign key from genpdf)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    company_id = db.Column(db.BigInteger, nullable=False)  # company_id, int8
    location_id = db.Column(db.BigInteger, nullable=False)  # location_id, int8

    # Relationships with other tables
    # Assuming that the foreign keys (cfd_id, xdata_id, genpdf_id) are related to other tables, 
    # we can use db.relationship to set up the relationships.
    # This is optional and depends on your specific needs for querying the related tables.

    # If the foreign keys relate to specific models:
    # cfd = db.relationship('Cfd', backref='master_core')
    # xdata = db.relationship('XData', backref='master_core')
    # genpdf = db.relationship('GenPdf', backref='master_core')

    def __repr__(self):
        return f"<MasterCore {self.id}>"
