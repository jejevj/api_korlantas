from ..extensions import db

class XData(db.Model):
    __tablename__ = 'xdata'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8
    master_id = db.Column(db.BigInteger, nullable=False)  # master_id, foreign key to master
    valid_content = db.Column(db.Boolean, nullable=False, default=False)  # valid_content, bool
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


    def __repr__(self):
        return f"<XData {self.merk} {self.tipe}>"
