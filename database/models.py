import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()


class Patient(db.Model):
    __tablename__ = "patients"
    mr = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    medical_history = db.Column(JSONB, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def represent(self):
        return f"<Patient {self.mr}: {self.first_name} {self.last_name}>"

    def __init__(self, **kwargs):
        super(Patient, self).__init__(**kwargs)
