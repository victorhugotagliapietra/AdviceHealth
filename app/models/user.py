from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
