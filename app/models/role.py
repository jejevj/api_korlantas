from ..extensions import db

class Role(db.Model):
    __tablename__ = "roles"  # Match your table name

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    changed_by = db.Column(db.String(50), default="system")
    caption = db.Column(db.String(20))

    def __repr__(self):
        return f"<Role {self.role}>"
