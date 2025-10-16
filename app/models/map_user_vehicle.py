from ..extensions import db

class MapUserVehicle(db.Model):
    __tablename__ = 'map_user_vehicle'

    # Columns mapping based on the provided schema
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)  # id column, type int8
    user_id = db.Column(db.BigInteger,  nullable=False)  # user_id, foreign key from users
    vehicle_id = db.Column(db.BigInteger, nullable=False)  # vehicle_id, foreign key from vehicles
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())  # created_at, timestamp
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # updated_at, timestamp
    changed_by = db.Column(db.String(255), nullable=False, default='pg_catalog')  # changed_by, varchar(255)

    def __repr__(self):
        return f"<MapUserVehicle User {self.user_id} Vehicle {self.vehicle_id}>"