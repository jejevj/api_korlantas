from ..extensions import db

class MobileBlacklistToken(db.Model):
    __tablename__ = "mobile_blacklist_token"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False)  # The blacklisted token
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp

    def __repr__(self):
        return f"<MobileBlacklistToken token={self.token}>"
