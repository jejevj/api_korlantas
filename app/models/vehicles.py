from ..extensions import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8
    status = db.Column(db.BigInteger, db.ForeignKey('statuses.id'), nullable=False)  # status, foreign key from statuses
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)  # user_id, foreign key from users
    cfd_id = db.Column(db.BigInteger, db.ForeignKey('cfd.id'), nullable=False)  # cfd_id, foreign key from cfd
    genpdf_id = db.Column(db.BigInteger, db.ForeignKey('genpdf.id'), nullable=False)  # genpdf_id, foreign key from genpdf
    merk = db.Column(db.String(20), nullable=False)  # merk, varchar(20)
    tipe = db.Column(db.String(100), nullable=False)  # tipe, varchar(100)
    jenis = db.Column(db.String(30), nullable=False)  # jenis, varchar(30)
    model = db.Column(db.String(50), nullable=False)  # model, varchar(50)
    tahun_pembuatan = db.Column(db.SmallInteger, nullable=False)  # tahun_pembuatan, int2
    isi_daya = db.Column(db.String(20), nullable=False)  # isi_daya, varchar(20)
    warna = db.Column(db.String(20), nullable=False)  # warna, varchar(20)
    bahan_bakar = db.Column(db.String(20), nullable=False)  # bahan_bakar, varchar(20)
    jumlah_sumbu = db.Column(db.SmallInteger, nullable=False)  # jumlah_sumbu, int2
    jumlah_roda = db.Column(db.SmallInteger, nullable=False)  # jumlah_roda, int2
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)
    verified_at = db.Column(db.TIMESTAMP, nullable=False)  # verified_at, timestamp
    sent_at = db.Column(db.TIMESTAMP, nullable=False)  # sent_at, timestamp
    verified_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # verified_by, varchar(50)

    # Relationships with other tables
    status_relation = db.relationship('Status', backref='vehicles')  # Status relation
    user_relation = db.relationship('User', backref='vehicles')  # User relation
    cfd_relation = db.relationship('Cfd', backref='vehicles')  # Cfd relation
    genpdf_relation = db.relationship('GenPdf', backref='vehicles')  # GenPdf relation

    def __repr__(self):
        return f"<Vehicle {self.merk} {self.tipe}>"
