from ..extensions import db

class Cfd(db.Model):
    __tablename__ = 'cfd'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True)  # id column, type int8 (primary key)
    master_id = db.Column(db.BigInteger, nullable=False)  # master_id, foreign key from master table
    valid_content = db.Column(db.Boolean, nullable=False, default=False)  # valid_content, bool
    jenis_ranmor = db.Column(db.SmallInteger, nullable=False)  # jenis_ranmor, int2 (valid value: 2/3 | 4/lebih)
    nomor_rangka = db.Column(db.String(20), nullable=False)  # nomor_rangka, varchar(20)
    nomor_mesin = db.Column(db.String(20), nullable=False)  # nomor_mesin, varchar(20)
    nomor_rangka_pic = db.Column(db.String(255), nullable=False)  # nomor_rangka_pic, varchar(255)
    nomor_mesin_pic = db.Column(db.String(255), nullable=False)  # nomor_mesin_pic, varchar(255)
    tampak_depan_pic = db.Column(db.String(255), nullable=False)  # tampak_depan_pic, varchar(255)
    tampak_belakang_pic = db.Column(db.String(255), nullable=False)  # tampak_belakang_pic, varchar(255)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(50), nullable=False, default='pg_catalog')  # changed_by, varchar(50)
    plat_nomor = db.Column(db.String(20), nullable=False)  # plat_nomor, varchar(20)

    def __repr__(self):
        return f"<Cfd {self.nomor_rangka}>"
