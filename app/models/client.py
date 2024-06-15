from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Client(db.Model):
  __tablename__ = 'clients'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(255), nullable=False)
  sales_opportunity = db.Column(db.Boolean, default=True, nullable=True)
  vehicles = db.relationship('Vehicle', backref='owner', lazy=True)
