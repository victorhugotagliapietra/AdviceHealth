from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Vehicle(db.Model):
  __tablename__ = 'vehicles'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  color = db.Column(db.Enum('YELLOW', 'BLUE', 'GRAY', name='color_enum'), nullable=False)
  model = db.Column(db.Enum('HATCH', 'SEDAN', 'CONVERTIBLE', name='model_enum'), nullable=False)
  client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('clients.id'), nullable=False)
